import RPi.GPIO as GPIO
import threading

# Define the GPIO pins used for PWM lighting control
PWM_PINS = [12, 13, 19]

# Frequency for PWM (Hz)
PWM_FREQ = 1000

# Dictionary to track brightness values from each source (e.g., 'v2v', 'lidar_camera')
brightness_sources = {
    'v2v': 100,
    'lidar_camera': 100
}

# Lock to ensure thread-safe access to brightness_sources
lock = threading.Lock()

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Initialize each PWM pin
for pin in PWM_PINS:
    GPIO.setup(pin, GPIO.OUT)

# Create a PWM object for each pin
pwm_channels = [GPIO.PWM(pin, PWM_FREQ) for pin in PWM_PINS]

# Start PWM with full brightness (100%)
for pwm in pwm_channels:
    pwm.start(100)

def apply_combined_brightness():
    """
    Combine brightness values from all sources by taking the minimum value.
    This ensures that if one source wants to dim the lights, the lights will dim.
    The brightness will never go to 0 to avoid turning off completely.
    """
    with lock:
        # Calculate the lowest brightness requested by any source
        combined_brightness = min(brightness_sources.values())

        # Enforce analog dimming: never allow 0% (off), use 1% as minimum
        effective_brightness = combined_brightness if combined_brightness > 0 else 1

        # Apply the effective brightness to all PWM channels
        for pwm in pwm_channels:
            pwm.ChangeDutyCycle(effective_brightness)

def set_source_brightness(source, value):
    """
    Set brightness from a specific source and re-evaluate the combined brightness.
    'source' is a string like 'v2v' or 'lidar_camera'.
    'value' should be an integer (100 for full, 1 for dim).
    """
    with lock:
        # Enforce analog dimming: treat any value <= 0 as 1
        brightness_sources[source] = value if value > 0 else 1
    apply_combined_brightness()

def cleanup():
    """
    Clean up PWM and GPIO when shutting down.
    """
    for pwm in pwm_channels:
        pwm.stop()
    GPIO.cleanup()
