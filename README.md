# Safety-Driven Headlight Control System

## Overview
The **Safety-Driven Headlight Control System** is an advanced automotive application that leverages computer vision and AI to enhance driving safety. Using a YOLOv11 model, this system dynamically adjusts vehicle headlights based on the detection and proximity of oncoming cars and pedestrians, reducing glare and improving visibility.

## Features
- 🚗 **Object Detection**: Identifies cars, pedestrians, and other vehicles in real-time.
- 🌌 **Dynamic Headlight Control**: Adjusts headlight intensity and direction based on detected objects.
- 📏 **Distance Measurement**: Uses YOLOv11's bounding box data to estimate distances.
- 💡 **Adaptive Lighting**: Minimizes glare for oncoming drivers while maintaining optimal visibility.

## Project Highlights
- **Model Accuracy**: Achieved 87% accuracy in object detection with YOLOv11.
- **Technologies Used**: 
  - YOLOv11 for real-time object detection.
  - Python for implementation.
  - CARLA Simulator for testing in a virtual driving environment.
- **Dataset**: Custom dataset annotated with Roboflow, consisting of vehicles and pedestrians.

## System Workflow
1. **Input**: Video feed from the vehicle's camera.
2. **Detection**: YOLOv11 identifies objects and their bounding boxes.
3. **Distance Estimation**: Calculates the proximity of detected objects.
4. **Control**: Adjusts headlight beam intensity and angle based on distance and type of detected object.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/safety-driven-headlight-control.git
