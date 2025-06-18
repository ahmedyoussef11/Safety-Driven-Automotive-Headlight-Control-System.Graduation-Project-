#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import serial
from enum import Enum
import struct
import RPi.GPIO as GPIO  # Added for GPIO control

# ----------------------------------------------------------------------
# System Constants
# ----------------------------------------------------------------------
SERIAL_PORT = "/dev/ttyS0"
MEASUREMENTS_PER_PLOT = 480
PLOT_MAX_RANGE = 4.0  # in meters
PLOT_AUTO_RANGE = False
PLOT_CONFIDENCE = True
PLOT_CONFIDENCE_COLOUR_MAP = "bwr_r"
PRINT_DEBUG = False
ANGLE_MIN = 0    # Minimum angle in degrees
ANGLE_MAX = 90  # Maximum angle in degrees (set to 180 for half-scan)

# GPIO setup
LED_PIN = 12  # GPIO pin number (you can change this if needed)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
pwm = GPIO.PWM(LED_PIN, 1000)  # 1000Hz PWM frequency
pwm.start(100)  # Start at 100% brightness

# ----------------------------------------------------------------------
# Main Packet Format
# ----------------------------------------------------------------------
PACKET_LENGTH = 47
MEASUREMENT_LENGTH = 12
MESSAGE_FORMAT = "<xBHH" + "HB" * MEASUREMENT_LENGTH + "HHB"

State = Enum("State", ["SYNC0", "SYNC1", "SYNC2", "LOCKED", "UPDATE_PLOT"])


def parse_lidar_data(data):
    length, speed, start_angle, *pos_data, stop_angle, timestamp, crc = \
        struct.unpack(MESSAGE_FORMAT, data)
    start_angle = float(start_angle) / 100.0
    stop_angle = float(stop_angle) / 100.0
    if stop_angle < start_angle:
        stop_angle += 360.0
    step_size = (stop_angle - start_angle) / (MEASUREMENT_LENGTH - 1)
    angle = [start_angle + step_size * i for i in range(MEASUREMENT_LENGTH)]
    distance = pos_data[0::2]  # in millimeters
    confidence = pos_data[1::2]
    if PRINT_DEBUG:
        print(length, speed, start_angle, *pos_data, stop_angle, timestamp, crc)
    return list(zip(angle, distance, confidence))


def get_xyc_data(measurements):
    # Filter measurements for angles between ANGLE_MIN and ANGLE_MAX
    filtered = [m for m in measurements if ANGLE_MIN <= m[0] <= ANGLE_MAX]
    angle = np.array([m[0] for m in filtered])
    distance = np.array([m[1] for m in filtered])
    confidence = np.array([m[2] for m in filtered])
    x = np.sin(np.radians(angle)) * (distance / 1000.0)
    y = np.cos(np.radians(angle)) * (distance / 1000.0)
    return x, y, confidence, distance


def adjust_led_brightness(distance_array):
    """Adjust LED brightness based on minimum distance."""
    if distance_array.size > 0:
        min_distance = np.min(distance_array) / 1000.0  # convert to meters
        if min_distance <= 1:
            pwm.ChangeDutyCycle(10)  # 10% brightness
        else:
            pwm.ChangeDutyCycle(100)  # 100% brightness


running = True


def on_plot_close(event):
    global running
    running = False


if __name__ == "__main__":
    try:
        lidar_serial = serial.Serial(SERIAL_PORT, 230400, timeout=0.5)
        measurements = []
        data = b''
        state = State.SYNC0

        # Plot setup
        plt.ion()
        plt.rcParams['figure.figsize'] = [10, 10]
        plt.rcParams['lines.markersize'] = 2.0
        if PLOT_CONFIDENCE:
            graph = plt.scatter([], [], c=[], marker=".", vmin=0,
                                vmax=255, cmap=PLOT_CONFIDENCE_COLOUR_MAP)
        else:
            graph = plt.plot([], [], ".")[0]
        graph.figure.canvas.mpl_connect('close_event', on_plot_close)
        plt.xlim(-PLOT_MAX_RANGE, PLOT_MAX_RANGE)
        plt.ylim(-PLOT_MAX_RANGE, PLOT_MAX_RANGE)

        # Main loop
        while running:
            if state == State.SYNC0:
                data = b''
                measurements = []
                if lidar_serial.read() == b'\x54':
                    data = b'\x54'
                    state = State.SYNC1

            elif state == State.SYNC1:
                if lidar_serial.read() == b'\x2C':
                    state = State.SYNC2
                    data += b'\x2C'
                else:
                    state = State.SYNC0

            elif state == State.SYNC2:
                data += lidar_serial.read(PACKET_LENGTH - 2)
                if len(data) != PACKET_LENGTH:
                    state = State.SYNC0
                    continue
                measurements += parse_lidar_data(data)
                state = State.LOCKED

            elif state == State.LOCKED:
                data = lidar_serial.read(PACKET_LENGTH)
                if data[0] != 0x54 or len(data) != PACKET_LENGTH:
                    print("WARNING: Serial sync lost")
                    state = State.SYNC0
                    continue
                measurements += parse_lidar_data(data)
                if len(measurements) > MEASUREMENTS_PER_PLOT:
                    state = State.UPDATE_PLOT

            elif state == State.UPDATE_PLOT:
                x, y, c, d = get_xyc_data(measurements)
                adjust_led_brightness(d)  # Adjust brightness based on distance

                if PLOT_AUTO_RANGE and x.size > 0 and y.size > 0:
                    max_val = max([max(abs(x)), max(abs(y))]) * 1.2
                    plt.xlim(-max_val, max_val)
                    plt.ylim(-max_val, max_val)

                graph.remove()
                if PLOT_CONFIDENCE:
                    graph = plt.scatter(x, y, c=c, marker=".",
                                        vmin=0, vmax=255,
                                        cmap=PLOT_CONFIDENCE_COLOUR_MAP)
                else:
                    graph = plt.plot(x, y, 'b.')[0]

                plt.pause(0.00001)
                state = State.LOCKED
                measurements = []

    except KeyboardInterrupt:
        print("\nStopping program...")

    finally:
        pwm.stop()
        GPIO.cleanup()  # Clean up GPIO
        lidar_serial.close()
        print("GPIO cleaned and serial closed.")
