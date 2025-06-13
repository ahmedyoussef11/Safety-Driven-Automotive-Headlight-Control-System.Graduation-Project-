![5947363368392312348](https://github.com/user-attachments/assets/ffd8ebbc-030d-4c46-a57a-e8a0456a8dfe)# Safety Driven Automotive Headlight Control System 🚗💡

Hi there! This is our graduation project from Obour High Institute – a smart adaptive headlight system designed to reduce nighttime accidents.

We used computer vision, LiDAR, and V2V (vehicle-to-vehicle) communication to automatically dim or adjust car headlights when other vehicles or people are nearby.

## Main Problem
The main problem addressed in this project is the danger caused by high-beam headlight glare during nighttime driving, which can temporarily blind oncoming drivers and significantly increase the risk of accidents. Many drivers forget or fail to switch to low beams in time, leading to reduced visibility, delayed reaction times, and potential collisions. This issue is especially critical on narrow or poorly lit roads where vehicles face each other directly. Current headlight systems lack intelligent, real-time adaptation, making it essential to develop an automated solution that minimizes glare without compromising the driver's own visibility.

## System Diagram Overview
![Screenshot 2025-06-13 150004](https://github.com/user-attachments/assets/0919a30a-c196-4204-93bc-df5d7f4ef337)


## Supervisors 
# Dr. Hayam Abdelmordy
![5929424934969396911](https://github.com/user-attachments/assets/d6d7c164-1483-465a-8ad7-e62244c8b5c2)

# Eng. Mostafa Ramadan 
![5947363368392312348](https://github.com/user-attachments/assets/93be389d-415a-430b-b1d9-0bda2edacffc)


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
