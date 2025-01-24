# **AI-based Safety-Driven Automotive Headlight Control System**

## **Project Overview**
This branch of the **Safety-Driven Automotive Headlight Control System** focuses on the **AI** components, specifically the **object detection** and **sensor fusion** algorithms used to enhance the vehicle’s headlight control system. The goal is to leverage AI models to detect obstacles (such as vehicles and pedestrians) and fuse sensor data (from camera, LIDAR, and V2V communication) to optimize the headlight functionality for improved safety.

---

## **Technologies Used in AI Branch**
- **YOLOv11 (You Only Look Once)**: A state-of-the-art real-time object detection model used to detect vehicles, pedestrians, and other objects.

---

## **AI Model - YOLOv11**
The **YOLOv11** object detection model is used for real-time object classification and detection, specifically for detecting the following objects:
- Vehicles (Cars, Trucks, Vans, etc.)
- Pedestrians

The model outputs bounding boxes with confidence scores for each detected object, which is then used by the **Headlight Control Node** to adjust the headlights accordingly.

### **Training YOLOv11**
The model was trained using [our Roboflow dataset](https://app.roboflow.com/customization-zusov/vehicle-and-pedestrian-cuisv/2) of vehicles and pedestrians.
---

## **Contributors to AI Branch**
- [Ahmed Youssef](https://github.com/ahmedyoussef11)
- [Aya Ahmed](https://github.com/ayaahmed31)
