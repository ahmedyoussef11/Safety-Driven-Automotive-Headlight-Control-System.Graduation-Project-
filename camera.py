import cv2
import tkinter as tk
from PIL import Image, ImageTk
from picamera2 import Picamera2
from ultralytics import YOLO
import threading
import time
import sys


def camera_init():
    """Initialize the PiCamera2."""
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()
    return picam2


def capture_frame(picam2, model, label):
    """Capture frames from camera, run YOLO inference, and update GUI frame."""
    while True:
        frame = picam2.capture_array()
        results = model.predict(frame)
        im = results[0].plot()

        # You can still check for detections, but no GPIO control here
        detected = any(
            int(box.cls[0]) in [0, 2]
            for result in results
            for box in result.boxes
        )

        # Update the GUI frame
        if im is not None:
            im = Image.fromarray(im)
            imgtk = ImageTk.PhotoImage(image=im)
            label.imgtk = imgtk
            label.configure(image=imgtk)


def run_detection():
    """Run the full detection and GUI display process (no GPIO)."""
    try:
        picam2 = camera_init()
        model = YOLO('yolov8n.pt')

        root = tk.Tk()
        root.title("YOLO Object Detection")
        label = tk.Label(root)
        label.pack()

        capture_thread = threading.Thread(
            target=capture_frame, args=(picam2, model, label), daemon=True
        )
        capture_thread.start()

        def update_frame():
            """Periodic frame update in GUI."""
            label.after(50, update_frame)

        update_frame()
        root.mainloop()

    except KeyboardInterrupt:
        print("\n[INFO] Program interrupted by user.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        print("[INFO] Exiting.")

if name == "__main__":
    run_detection()
