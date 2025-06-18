#!/usr/bin/env python3
# -- coding: utf-8 --
# lidar_camera.py
import time
import threading
import serial
import struct
from enum import Enum
from picamera2 import Picamera2  # Raspberry Pi Camera library
from ultralytics import YOLO     # YOLO object detection
import shared_led_control as led # Custom LED control module

# Serial port configuration for Lidar
SERIAL_PORT = "/dev/ttyS0"
# Number of measurements per plot/sweep
MEASUREMENTS_PER_PLOT = 480
# Angular range for filtering Lidar data
ANGLE_MIN = 30
ANGLE_MAX = 90
# Distance threshold in meters (8cm converted to meters)
DISTANCE_THRESHOLD = 0.8
# Packet structure constants
PACKET_LENGTH = 47
MEASUREMENT_LENGTH = 12
# Binary data format for unpacking Lidar packets
MESSAGE_FORMAT = "<xBHH" + "HB" * MEASUREMENT_LENGTH + "HHB"

# COCO dataset class IDs for objects we care about
RELEVANT_CLASSES = {
    0: 'person',
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck'
}

# Finite State Machine states for parsing Lidar data
State = Enum("State", ["SYNC0", "SYNC1", "SYNC2", "LOCKED", "UPDATE_DATA"])

def parse_lidar_data(data):
    """Unpacks raw Lidar packet data into structured measurements"""
    length, speed, start_angle, *pos_data, stop_angle, timestamp, crc = \
        struct.unpack(MESSAGE_FORMAT, data)
    # Convert angles from hundredths to degrees
    start_angle = float(start_angle) / 100.0
    stop_angle = float(stop_angle) / 100.0
    # Handle angle wrap-around
    if stop_angle < start_angle:
        stop_angle += 360.0
    # Calculate intermediate angles
    step_size = (stop_angle - start_angle) / (MEASUREMENT_LENGTH - 1)
    angle = [start_angle + step_size * i for i in range(MEASUREMENT_LENGTH)]
    # Separate distance and confidence values
    distance = pos_data[0::2]
    confidence = pos_data[1::2]
    # Combine into list of (angle, distance, confidence) tuples
    return list(zip(angle, distance, confidence))

def filter_measurements(measurements):
    """Filters measurements to only include those within desired angular range"""
    return [m for m in measurements if ANGLE_MIN <= m[0] <= ANGLE_MAX]

def take_action(detected_object, distance):
    """Function to execute when conditions are met"""
    print(f"ALERT: {detected_object} detected at {distance:.2f} meters!")
    # Here you can add any action you want to take:
    # - Sound a buzzer
    # - Send a notification
    # - Trigger an external device
    # Example:
    # GPIO.output(BUZZER_PIN, GPIO.HIGH)
    # time.sleep(0.5)
    # GPIO.output(BUZZER_PIN, GPIO.LOW)

# Initialize Raspberry Pi camera
picam2 = Picamera2()
# Configure camera with 640x480 resolution
picam2.configure(picam2.create_preview_configuration(
    main={'size': (640, 480), 'format': 'RGB888'}))
picam2.start()  # Start camera stream

# Load YOLOv8 Nano model for object detection
model = YOLO('/yolov8n.pt')
# Global variables for object detection
detected_objects = []
object_detected = False

def capture_and_process():
    """Thread function for continuous camera capture and object detection"""
    global detected_objects, object_detected
    while True:
        # Capture frame from camera
        frame = picam2.capture_array()
        # Run object detection
        results = model(frame)
        
        # Reset detected objects list
        detected_objects = []
        
        # Check for relevant objects
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                if class_id in RELEVANT_CLASSES:
                    detected_objects.append(RELEVANT_CLASSES[class_id])
        
        # Update detection status
        object_detected = bool(detected_objects)
        time.sleep(0.1)  # Control processing rate

def process_lidar():
    """Thread function for Lidar data processing"""
    try:
        # Initialize serial connection to Lidar
        lidar_serial = serial.Serial(SERIAL_PORT, 230400, timeout=0.5)
        measurements = []  # Stores accumulated measurements
        data = b''         # Raw data buffer
        state = State.SYNC0  # Initial state machine state

        while True:
            if state == State.SYNC0:
                # Reset and look for packet start byte (0x54)
                data = b''
                measurements = []
                if lidar_serial.read() == b'\x54':
                    data = b'\x54'
                    state = State.SYNC1

            elif state == State.SYNC1:
                # Verify second sync byte (0x2C)
                if lidar_serial.read() == b'\x2C':
                    data += b'\x2C'
                    state = State.SYNC2
                else:
                    state = State.SYNC0  # Sync failed, reset

            elif state == State.SYNC2:
                # Read remaining packet bytes
                data += lidar_serial.read(PACKET_LENGTH - 2)
                if len(data) != PACKET_LENGTH:
                    state = State.SYNC0  # Incomplete packet
                    continue
                # Parse valid packet
                measurements += parse_lidar_data(data)
                state = State.LOCKED

            elif state == State.LOCKED:
                # Read subsequent packets
                data = lidar_serial.read(PACKET_LENGTH)
                if data[0] != 0x54 or len(data) != PACKET_LENGTH:
                    print("WARNING: Serial sync lost")
                    state = State.SYNC0  # Sync lost, reset
                    continue
                measurements += parse_lidar_data(data)
                # When enough measurements collected, process them
                if len(measurements) > MEASUREMENTS_PER_PLOT:
                    state = State.UPDATE_DATA

            elif state == State.UPDATE_DATA:
                # Filter measurements and check for objects
                filtered = filter_measurements(measurements)
                distances = [m[1]/1000.0 for m in filtered]  # Convert to meters
                
                # If object detected and within threshold distance
                if object_detected and distances and min(distances) <= DISTANCE_THRESHOLD:
                    led.set_source_brightness('lidar', 0)  # Dim LED
                    # Take action for each detected object
                    for obj in set(detected_objects):  # Use set to avoid duplicates
                        take_action(obj, min(distances))
                else:
                    led.set_source_brightness('lidar', 100)  # Full brightness
                
                state = State.LOCKED
                measurements = []  # Reset for next batch

    except KeyboardInterrupt:
        print("Stopping lidar thread...")
    finally:
        # Cleanup resources
        lidar_serial.close()
        led.cleanup()

if __name__ == '__main__':
    # Start camera processing thread
    threading.Thread(target=capture_and_process, daemon=True).start()
    # Start Lidar processing thread
    threading.Thread(target=process_lidar, daemon=True).start()
    try:
        # Main thread just sleeps while workers run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting lidar-camera script")
        led.cleanup()
