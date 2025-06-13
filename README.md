# Safety Driven Automotive Headlight Control System 🚗💡

Hi there! This is our graduation project from Obour High Institute – a smart adaptive headlight system designed to reduce nighttime accidents.

We used computer vision, LiDAR, and V2V (vehicle-to-vehicle) communication to automatically dim or adjust car headlights when other vehicles or people are nearby.

## Main Problem
The main problem addressed in this project is the danger caused by high-beam headlight glare during nighttime driving, which can temporarily blind oncoming drivers and significantly increase the risk of accidents. Many drivers forget or fail to switch to low beams in time, leading to reduced visibility, delayed reaction times, and potential collisions. This issue is especially critical on narrow or poorly lit roads where vehicles face each other directly. Current headlight systems lack intelligent, real-time adaptation, making it essential to develop an automated solution that minimizes glare without compromising the driver's own visibility.
![Screenshot_2025-06-13_150004-removebg-preview](https://github.com/user-attachments/assets/201c5034-a28d-472d-b841-8f55c118d99e)

## System Diagram Overview
- Raspberry Pi 4 (main controller)
- Pi Camera 3 NoIR (night vision)
- OKdo LiDAR HAT (distance sensor)
- LoRa SX1278 modules (for V2V messaging)
- Python (main language)
- YOLOv8 (for real-time object detection)
- Tkinter (to show a live camera feed + detections)

## 📁 Project Structure
This repo has 3 branches:

- `ai` → training the YOLO model (includes Roboflow, Kaggle links, etc.)
- `embedded-sys` → code for Raspberry Pi (LiDAR, LED, GUI)
- `v2v` → LoRa-based messaging between vehicles

## 🧠 How We Built It
- Collected our own dataset for car lights, pedestrians, and vehicles at night
- Labeled it using Roboflow
- Trained a YOLOv8 model on Kaggle (it’s small enough to run on Raspberry Pi!)
- Connected the Pi Camera and LiDAR together
- Wrote code to sync detections with distance and control an LED
- Set up LoRa between two Pis to simulate two cars communicating

## 🙋‍♂️ Team
We're 5 students from the Communications and Electronics Department:

- [Ahmed Youssef](https://github.com/ahmedyoussef11) – AI
- [Aya Sayed Ahmed](https://github.com/ayaahmed31) - AI
- [Abdallah Hossam](https://github.com/AbdallahHossamRamzy) – Embedded coding 
- [Ahmed Moustafa](https://github.com/Ahmedelkbany) – V2V
- [Omar Mohammed](https://github.com/Omar-Mo7ammed) – V2V

---

Thanks for reading! 😄
Feel free to message us if you're working on something similar!
