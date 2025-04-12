# 🚘 AI Module 

This branch contains the AI module of our ADAS project. We trained a custom object detection model using YOLOv8 to identify road elements like pedestrians, vehicles, lanes, and signs in real-time.

---

## 💡 Why YOLOv8?
We tried different models, but YOLOv8n (the Nano version) gave us the best balance between speed and accuracy — and it actually runs well on Raspberry Pi with some tweaks.

## 🧠 Dataset
We built the dataset ourselves:
- Collected real-world images 
- Annotated using **Roboflow**
- Classes: `car`, `person`, `bike`, `traffic_sign`, etc.

You can find the dataset versioned on [Roboflow]([https://roboflow.com](https://app.roboflow.com/project-mzmwg/street-objects-ag7dt/browse?queryText=&pageSize=200&startingIndex=0&browseQuery=true)).

