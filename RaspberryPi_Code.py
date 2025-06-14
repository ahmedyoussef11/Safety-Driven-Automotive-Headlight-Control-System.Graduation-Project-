import json
import time
import threading
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import smbus2
import math

# === PWM setup ===
PWM_PINS = [12, 13, 19]
PWM_FREQ = 1000

GPIO.setmode(GPIO.BCM)
for pin in PWM_PINS:
    GPIO.setup(pin, GPIO.OUT)

pwm_channels = [GPIO.PWM(pin, PWM_FREQ) for pin in PWM_PINS]
for pwm in pwm_channels:
    pwm.start(100)  # Full brightness

# === MQTT configuration ===
MQTT_BROKER = "192.168.50.1"
MQTT_PORT = 1883
TOPIC_SIGNAL = "car2/signal"
TOPIC_ESP32_HEADING = "car/esp32_heading"
TOPIC_PI_HEADING = "car/pi_heading"

# === State variables ===
car_rssi = None
last_seen = 0
STALE_TIMEOUT = 10
state = 'idle'
largest_rssi = None
esp32_heading = None
pi_heading = None

# === I2C & Magnetometer ===
bus = smbus2.SMBus(1)
hmc_address = 0x1E

def hmc_init():
    bus.write_byte_data(hmc_address, 0x00, 0x70)
    bus.write_byte_data(hmc_address, 0x01, 0xA0)
    bus.write_byte_data(hmc_address, 0x02, 0x00)

def read_word(address, reg):
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        val -= 0x10000
    return val

def read_data_x_axis_only():
    x = read_word(hmc_address, 0x03)
    heading = (x + 2048) * (360.0 / 4096)
    return heading % 360

def set_brightness(percent):
    for pwm in pwm_channels:
        pwm.ChangeDutyCycle(percent)

def is_heading_opposite():
    if pi_heading is not None and esp32_heading is not None:
        diff = abs(esp32_heading - pi_heading)
        if diff > 180:
            diff = 360 - diff
        print(f"Angle Difference: {diff:.2f} degrees")
        return 90 < diff < 270
    return False

def reset_to_initial_state():
    global car_rssi, largest_rssi, state
    print("ðŸ”„ Resetting to initial state")
    set_brightness(100)
    car_rssi = None
    largest_rssi = None
    state = 'idle'

def update_pwm_brightness():
    global car_rssi, state, largest_rssi

    threshold = -50
    margin = 4

    while True:
        if car_rssi is not None:
            print(f"RSSI: {car_rssi} dBm | Peak: {largest_rssi} dBm | State: {state}")

            if state == 'idle':
                if car_rssi > threshold and is_heading_opposite():
                    print("ðŸ”” Car approaching in opposite direction: dimming lights")
                    set_brightness(0)
                    state = 'action'
                    largest_rssi = car_rssi

            elif state == 'action':
                if car_rssi > largest_rssi:
                    largest_rssi = car_rssi
                elif car_rssi < largest_rssi - margin:
                    print("ðŸš— Car moving away: restoring lights")
                    set_brightness(100)
                    state = 'cooldown'

            elif state == 'cooldown':
                if car_rssi < threshold:
                    print("âœ… Car out of range: rearming detection")
                    state = 'idle'
                    largest_rssi = None

        time.sleep(0.1)

def on_message(client, userdata, msg):
    global car_rssi, last_seen, esp32_heading

    topic = msg.topic
    payload = msg.payload.decode()

    if topic == TOPIC_SIGNAL:
        try:
            data = json.loads(payload)
            rssi = int(data.get("rssi", -100))
            car_rssi = rssi
            last_seen = time.time()
        except Exception as e:
            print(f"Error parsing RSSI message: {e}")

    elif topic == TOPIC_ESP32_HEADING:
        try:
            esp32_heading = float(payload)
            print(f"Received ESP32 Heading: {esp32_heading:.2f}")
        except ValueError:
            print("Invalid heading received from ESP32.")

def monitor_stale_data():
    global car_rssi
    while True:
        if time.time() - last_seen > STALE_TIMEOUT:
            if car_rssi is not None:
                print("âŒ Connection lost: RSSI signal stale")
                reset_to_initial_state()
        time.sleep(1)

def publish_pi_heading(client):
    global pi_heading
    while True:
        pi_heading = read_data_x_axis_only()
        print(f"Pi Heading (X-axis only): {pi_heading:.2f}")
        client.publish(TOPIC_PI_HEADING, str(pi_heading))
        time.sleep(0.5)

def main():
    hmc_init()

    client = mqtt.Client()
    client.on_message = on_message

    try:
        print("Connecting to MQTT broker...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("Connected successfully.")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    client.subscribe(TOPIC_SIGNAL)
    client.subscribe(TOPIC_ESP32_HEADING)

    threading.Thread(target=update_pwm_brightness, daemon=True).start()
    threading.Thread(target=monitor_stale_data, daemon=True).start()
    threading.Thread(target=publish_pi_heading, args=(client,), daemon=True).start()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for pwm in pwm_channels:
            pwm.stop()
        GPIO.cleanup()
        print("GPIO cleaned up. Exiting...")

if __name__ == "__main__":
    main()
