#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from picamera2 import Picamera2
from ultralytics import YOLO
import threading
import RPi.GPIO as GPIO
import time

# Set up GPIO for LED control using PWM
LED_PIN = 19  # GPIO pin connected to the LED
BUZZER_PIN = 26  # Add a buzzer pin for alerts
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(LED_PIN, 10000)  # 1000Hz PWM frequency for smooth dimming
pwm.start(100)  # Start at 100% brightness

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load YOLO model
model = YOLO('best.pt')

# Dataset class IDs for objects we care about
RELEVANT_CLASSES = {
    0: 'person',
    2: 'car',
    # 3: 'motorcycle',
    # 5: 'bus',
    7: 'truck'
}

# Set up GUI
root = tk.Tk()
root.title("YOLO Object Detection")
label = tk.Label(root)
label.pack()

last_frame = None
alert_active = False
last_alert_time = 0
alert_cooldown = 3  # seconds between alerts for the same object

def trigger_alert(object_type):
    """Function to execute when relevant objects are detected"""
    global alert_active, last_alert_time
    
    current_time = time.time()
    if current_time - last_alert_time < alert_cooldown:
        return  # Skip if we recently triggered an alert
    
    print(f"ALERT: {object_type} detected!")
    last_alert_time = current_time
    
    # Visual alert (LED blinking)
    alert_active = True
    for _ in range(3):  # Blink 3 times
        if not alert_active:  # Allow early exit
            break
        pwm.ChangeDutyCycle(10)  # Dim
        GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Sound buzzer
        time.sleep(0.2)
        pwm.ChangeDutyCycle(100)  # Bright
        GPIO.output(BUZZER_PIN, GPIO.LOW)  # Silence buzzer
        time.sleep(0.2)
    alert_active = False

def capture_frame():
    """Capture frames from camera and run YOLO inference."""
    global last_frame, alert_active
    
    while True:
        frame = picam2.capture_array()

        # Run YOLO inference
        results = model.predict(frame)
        im = results[0].plot()

        # Check for relevant objects
        detected_objects = set()
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                if class_id in RELEVANT_CLASSES:
                    detected_objects.add(RELEVANT_CLASSES[class_id])

        # Adjust LED brightness based on detection
        if detected_objects:
            pwm.ChangeDutyCycle(10)  # 10% brightness if relevant object detected
            
            # Trigger alert for each new object type
            for obj_type in detected_objects:
                if not alert_active:  # Only trigger if not already alerting
                    threading.Thread(target=trigger_alert, args=(obj_type,)).start()
        else:
            pwm.ChangeDutyCycle(100)  # 100% brightness otherwise
            alert_active = False  # Cancel any ongoing alert

        last_frame = im

def update_frame():
    """Update the GUI with the latest camera frame."""
    global last_frame
    if last_frame is not None:
        im = Image.fromarray(last_frame)
        imgtk = ImageTk.PhotoImage(image=im)
        label.imgtk = imgtk
        label.configure(image=imgtk)

    label.after(50, update_frame)

# Start threads
capture_thread = threading.Thread(target=capture_frame, daemon=True)
capture_thread.start()

update_frame()
try:
    root.mainloop()
finally:
    # Clean up GPIO when exiting
    alert_active = False  # Stop any ongoing alerts
    pwm.stop()
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.cleanup()
