#!/usr/bin/env python3
# -- coding: utf-8 --

# lidar_camera_with_stop sign_gpio.py

import time
import threading
import serial
import struct
from enum import Enum
from picamera2 import Picamera2              # Raspberry Pi Camera library
from ultralytics import YOLO                 # YOLO object detection
import RPi.GPIO as GPIO                      # GPIO for Raspberry Pi
import shared_led_control as led             # Custom LED control module

# ---------- Lidar Serial Configuration ----------
SERIAL_PORT = "/dev/ttyS0"
MEASUREMENTS_PER_PLOT = 480
ANGLE_MIN = 30
ANGLE_MAX = 90
DISTANCE_THRESHOLD = 0.8  # meters
PACKET_LENGTH = 47
MEASUREMENT_LENGTH = 12
MESSAGE_FORMAT = "<xBHH" + "HB" * MEASUREMENT_LENGTH + "HHB"

# ---------- YOLO COCO Classes of Interest ----------
RELEVANT_CLASSES = {
    0: 'person',
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck'
}

CELLPHONE_CLASS_ID = 11  # COCO class for "stop sign"

# ---------- GPIO Setup ----------
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)  # Pin 20 for stop sign detection trigger

# ---------- Lidar Packet Parser State Machine ----------
State = Enum("State", ["SYNC0", "SYNC1", "SYNC2", "LOCKED", "UPDATE_DATA"])

def parse_lidar_data(data):
    """Unpacks raw Lidar packet data into structured measurements"""
    length, speed, start_angle, *pos_data, stop_angle, timestamp, crc = \
        struct.unpack(MESSAGE_FORMAT, data)
    start_angle = float(start_angle) / 100.0
    stop_angle = float(stop_angle) / 100.0
    if stop_angle < start_angle:
        stop_angle += 360.0
    step_size = (stop_angle - start_angle) / (MEASUREMENT_LENGTH - 1)
    angle = [start_angle + step_size * i for i in range(MEASUREMENT_LENGTH)]
    distance = pos_data[0::2]
    confidence = pos_data[1::2]
    return list(zip(angle, distance, confidence))

def filter_measurements(measurements):
    """Filters measurements to only include those within desired angular range"""
    return [m for m in measurements if ANGLE_MIN <= m[0] <= ANGLE_MAX]

def take_action(detected_object, distance):
    """Action when object is detected within threshold"""
    print(f"ALERT: {detected_object} detected at {distance:.2f} meters!")

# ---------- Camera Setup ----------
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={'size': (640, 480), 'format': 'RGB888'}))
picam2.start()

# Load YOLOv8 Nano model
model = YOLO('/yolov8n.pt')

# Global detection flags
detected_objects = []
object_detected = False
cellphone_detected = False

def capture_and_process():
    """Thread for continuous camera capture and object detection"""
    global detected_objects, object_detected, cellphone_detected

    while True:
        frame = picam2.capture_array()         # Capture frame
        results = model(frame)                 # Run YOLO

        detected_objects = []                  # Reset
        cellphone_detected = False             # Reset

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                if class_id in RELEVANT_CLASSES:
                    detected_objects.append(RELEVANT_CLASSES[class_id])
                elif class_id == CELLPHONE_CLASS_ID:
                    cellphone_detected = True  # Trigger GPIO 20

        object_detected = bool(detected_objects)

        # Handle GPIO 20 for cellphone detection
        if cellphone_detected:
            GPIO.output(20, GPIO.HIGH)
        else:
            GPIO.output(20, GPIO.LOW)

        time.sleep(0.1)

def process_lidar():
    """Thread for LiDAR processing"""
    try:
        lidar_serial = serial.Serial(SERIAL_PORT, 230400, timeout=0.5)
        measurements = []
        data = b''
        state = State.SYNC0

        while True:
            if state == State.SYNC0:
                data = b''
                measurements = []
                if lidar_serial.read() == b'\x54':
                    data = b'\x54'
                    state = State.SYNC1

            elif state == State.SYNC1:
                if lidar_serial.read() == b'\x2C':
                    data += b'\x2C'
                    state = State.SYNC2
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
                    state = State.UPDATE_DATA

            elif state == State.UPDATE_DATA:
                filtered = filter_measurements(measurements)
                distances = [m[1] / 1000.0 for m in filtered]

                if object_detected and distances and min(distances) <= DISTANCE_THRESHOLD:
                    led.set_source_brightness('lidar', 0)
                    for obj in set(detected_objects):
                        take_action(obj, min(distances))
                else:
                    led.set_source_brightness('lidar', 100)

                state = State.LOCKED
                measurements = []

    except KeyboardInterrupt:
        print("Stopping lidar thread...")
    finally:
        lidar_serial.close()
        led.cleanup()
        GPIO.cleanup()

# ---------- Main Program ----------
if __name__ == '__main__':
    threading.Thread(target=capture_and_process, daemon=True).start()
    threading.Thread(target=process_lidar, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program")
        led.cleanup()
        GPIO.cleanup()
