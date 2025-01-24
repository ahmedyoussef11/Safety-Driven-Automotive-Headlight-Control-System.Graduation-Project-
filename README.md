# **Safety-Driven Automotive Headlight Control System**

## **Project Overview**
The **Safety-Driven Automotive Headlight Control System** is an advanced vehicle safety feature aimed at improving night driving and low-visibility conditions. By leveraging **sensor fusion** (using cameras, LIDAR, and V2V communication), the system dynamically adjusts the headlights to improve road visibility, enhance situational awareness, and ensure driver safety.

This project integrates the **YOLOv11 object detection model**, **LIDAR data**, and **Vehicle-to-Vehicle (V2V) communication** to create a seamless and intelligent headlight control system.

---

## **Key Features**
- **Dynamic Headlight Control**: Automatically adjusts headlight intensity and direction based on real-time sensor data.
- **Object Detection**: Uses YOLOv11 for real-time object detection through camera images.
- **LIDAR Integration**: Provides precise distance measurements for improved depth perception.
- **V2V Communication**: Enables communication between vehicles to share real-time data (position, speed, and detected objects) for enhanced situational awareness.
- **Sensor Fusion**: Combines data from multiple sensors to provide a cohesive understanding of the environment.

---

## **Technologies Used**
- **YOLOv11 (You Only Look Once)**: A state-of-the-art object detection algorithm for detecting vehicles, pedestrians, and other obstacles.
- **LIDAR (Light Detection and Ranging)**: For accurate distance and depth perception.
- **V2V Communication**: Vehicle-to-Vehicle communication to enhance environmental awareness.
- **ROS (Robot Operating System)**: For managing and integrating sensors, controlling the headlight system, and handling real-time data processing.
- **Python**: The programming language used for the development of the ROS nodes.

---

## **Project Architecture**
The system is built around multiple ROS nodes that interact with the sensors and control the vehicle’s headlights based on processed data.

### **Nodes**
1. **Camera Node**: Captures video from the vehicle's camera and processes it using the YOLOv11 object detection model.
2. **LIDAR Node**: Processes LIDAR data to measure distances and detect objects.
3. **V2V Node**: Handles incoming Vehicle-to-Vehicle communication for external awareness.
4. **Headlight Control Node**: Adjusts the headlight intensity and direction based on fused sensor data.

### **Launch File**
A launch file (`all_nodes.launch`) is provided to start all ROS nodes simultaneously. This ensures smooth coordination between sensors and headlight control.

---

## **Getting Started**
Follow the instructions below to set up and run the **Safety-Driven Headlight Control System** locally.

### **Prerequisites**
- **ROS Noetic** (or another compatible ROS version)
- **Python 3** and the required Python packages (`rospy`, `sensor_msgs`, `cv_bridge`, etc.)
- **YOLOv11 model** for object detection (pre-trained weights)
- **LIDAR sensor** and **V2V communication system** (simulated or real)

### **Setup Instructions**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/ahmedyoussef11/SAFETY-DRIVEN-AUTOMOTIVE-HEADLIGHT-CONTROL-SYSTEM.git
   cd SAFETY-DRIVEN-AUTOMOTIVE-HEADLIGHT-CONTROL-SYSTEM
