# AI Model Selection 

This branch provides the custom-trained YOLOv8 model and dataset used in the Safety-Driven Automotive Headlight Control System project. The system is designed to detect vehicles, pedestrians, and road elements in real time using camera input on a Raspberry Pi. With high accuracy and lightweight performance, the AI model plays a central role in dynamically adjusting headlight intensity to reduce glare and enhance nighttime driving safety.

---

## Dataset Selection
We collected and managed a dataset of 3,618 images using Roboflow, which provided a streamlined interface for organizing, annotating, and preparing the data. The dataset includes seven object classes essential for nighttime driving scenarios: Car (3,736), Person (2,479), Traffic Light (1,007), Truck (916), Bicycle (675), Speed Limit 30 (537), and Stop Sign (531), ensuring comprehensive coverage of real-world traffic elements.

## Annotation Process
We annotated the dataset by drawing bounding boxes around each object of interest and labeling them according to their class type, such as car, bicycle, or person, to ensure accurate detection during model training.
![Screenshot 2025-06-08 175200](https://github.com/user-attachments/assets/c6688da0-9cd0-4d8e-898a-e8d6a1db6a42)

## Augmentation Process
To make our dataset better, we added some changes to the images using augmentation techniques.
These techniques included:
- Brightness and Contrast Adjustments.
- Blurring.

## Why YOLO?
YOLO (You Only Look Once) is a fast and efficient object detection model that divides an image into grids and predicts objects in one pass. 
Key Points:
     - Grid-based, single-pass detection.
     - Real-time performance.
     - Uses anchor boxes for accuracy.
     - Works well on embedded devices.

## Confusion Matrix
![confusion_matrix (1)](https://github.com/user-attachments/assets/e262d236-b859-466a-ae6f-3b9a38a51aa8)

## Precision Curve
![P_curve](https://github.com/user-attachments/assets/52aae3ce-12e1-4ce6-81b9-62a2f09be667)

## Recall Curve
![R_curve](https://github.com/user-attachments/assets/65d3b4c7-0fae-4e57-b1d6-547ab6ba2f83)

## F1 Score Curve
![F1_curve](https://github.com/user-attachments/assets/3ba8baad-6d00-43c9-8c6b-895311af8011)

## mAP50
![PR_curve](https://github.com/user-attachments/assets/ccc0b149-7da0-4332-b451-b6c6f3b4ed57)


## Results
![train_batch1](https://github.com/user-attachments/assets/ef0931a8-fc72-4cd1-9dd0-2dbdc3ef112d)![train_batch2](https://github.com/user-attachments/assets/a3d56a4a-176f-4780-aff4-e74fc9a9e46d)

![val_batch1_labels](https://github.com/user-attachments/assets/dce2f376-77b8-4080-9dd2-8bd0dc663c4b)



You can find the dataset versioned on [Roboflow]([https://roboflow.com](https://app.roboflow.com/project-mzmwg/street-objects-ag7dt/browse?queryText=&pageSize=200&startingIndex=0&browseQuery=true)).

