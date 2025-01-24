
# **AI-based Safety-Driven Automotive Headlight Control System**

## **Project Overview**
This branch of the **Safety-Driven Automotive Headlight Control System** focuses on the **AI** components, specifically the **object detection** and **sensor fusion** algorithms used to enhance the vehicle’s headlight control system. The goal is to leverage AI models to detect obstacles (such as vehicles and pedestrians) and fuse sensor data (from camera, LIDAR, and V2V communication) to optimize the headlight functionality for improved safety.

---

## **Technologies Used in AI Branch**
- **YOLOv11 (You Only Look Once)**: A state-of-the-art real-time object detection model used to detect vehicles, pedestrians, and other objects.
- **TensorFlow / PyTorch**: For training and deploying deep learning models.
- **OpenCV**: Used for image preprocessing, object tracking, and managing video feeds.
- **Sensor Fusion**: Combines data from the **LIDAR** and **camera** sensors to make accurate decisions based on object distances and visibility.

---

## **AI Model - YOLOv11**
The **YOLOv11** object detection model is used for real-time object classification and detection, specifically for detecting the following objects:
- Vehicles (Cars, Trucks, Vans, etc.)
- Pedestrians
- Road obstacles

The model outputs bounding boxes with confidence scores for each detected object, which is then used by the **Headlight Control Node** to adjust the headlights accordingly.

### **Training YOLOv11**
The model was trained using a custom dataset of vehicles and pedestrians. Training was done using **Roboflow** for dataset preparation and **PyTorch** for training. The following steps outline the training process:
1. **Data Annotation**: Manually annotating images of vehicles and pedestrians.
2. **Data Augmentation**: Performing transformations on the data to improve generalization (flipping, rotating, scaling).
3. **Model Training**: Using PyTorch and pre-trained weights to train the YOLOv11 model.

---

## **Getting Started with the AI Branch**

### **Prerequisites**
- **Python 3** and the required Python packages (`opencv-python`, `torch`, `pytorch-lightning`, `cv_bridge`, etc.)
- **YOLOv11 Pre-trained Weights** (Available in the repository)
- **LIDAR data** (simulated or real) for sensor fusion

### **Setup Instructions for AI Branch**

1. Clone the repository and switch to the AI branch:
   ```bash
   git clone https://github.com/ahmedyoussef11/SAFETY-DRIVEN-AUTOMOTIVE-HEADLIGHT-CONTROL-SYSTEM.git
   cd SAFETY-DRIVEN-AUTOMOTIVE-HEADLIGHT-CONTROL-SYSTEM
   git checkout ai-branch
   ```

2. Install the required Python dependencies:
   ```bash
   pip install opencv-python torch pytorch-lightning cv_bridge
   ```

3. Download the pre-trained YOLOv11 weights:
   - You can download the weights from the [official YOLOv11 repository](https://github.com/ultralytics/yolov5/releases) or use the provided `weights` folder.

4. Run the AI model:
   To test the object detection model, run the following script:
   ```bash
   python ai_model_inference.py
   ```
   This will load the camera feed, run the YOLOv11 object detection, and display the results.

---

## **Contributors to AI Branch**
- **Ahmed Youssef** – AI Developer and Researcher
- **Aya Ahmed** – Contributor
- **[Add more contributors here]**

---

## **Future Enhancements in AI Branch**
- **Improve Object Detection**: Implement better model architectures like **YOLOv4** or **EfficientDet** for higher accuracy.
- **Real-time Object Tracking**: Add a tracking system to track detected objects across multiple frames.
- **Sensor Fusion Optimization**: Develop advanced algorithms to more effectively fuse LIDAR, camera, and V2V data.

---

## **License**
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
