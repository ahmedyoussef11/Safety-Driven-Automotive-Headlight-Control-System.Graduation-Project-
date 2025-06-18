# LiDAR-Based Object Detection System

This repository contains the code and documentation for the LiDAR system used in our smart automotive headlight control project. The system is designed to detect objects in front of the vehicle using a 360° LiDAR sensor and control the headlight accordingly to minimize glare and enhance night-driving safety.

![Okdo-Lidar-Module-LiDAR-LD06-with-Bracket-Development-Kit-for-Raspberry-Pi-4B jpg_-1-removebg-preview](https://github.com/user-attachments/assets/ff95dacb-4641-42b5-96e1-443ac7ceee87)

---

## LiDAR Overview

- Utilizes a 360° OKdo LiDAR HAT (LD06_LD) for real-time object detection.
- Filters LiDAR readings to focus on specific angles (front-facing area).
- Computes object distance and triggers headlight dimming when needed.
- Designed to run on a Raspberry Pi for embedded real-time applications.

---

## Integration with Camera-Based Detection

The LiDAR system operates in parallel with a vision-based module that uses a Raspberry Pi Camera Module 3 NoIR paired with a YOLOv8 object detection model. While the LiDAR provides 360° distance measurements and detects any physical object within range, the camera adds contextual awareness by identifying specific classes such as cars, pedestrians, and traffic signs. To avoid unnecessary headlight dimming caused by irrelevant objects (e.g., trees, poles), the system integrates both inputs using a filtering logic: only when an object is detected both visually (by YOLO) and spatially (by LiDAR within a specific angular range and distance) will the headlight dimming logic be activated. This sensor-level fusion enhances accuracy, minimizes false positives, and ensures that the headlights adapt only to relevant and safety-critical detections.
