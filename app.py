import cv2
import numpy as np
import mediapipe as mp
import gradio as gr

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Load Face Detector
base_options = python.BaseOptions(model_asset_path=None)
face_detector = vision.FaceDetector.create_from_options(
    vision.FaceDetectorOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE
    )
)

def process_frame(image):
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    h, w, _ = img.shape

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    detection_result = face_detector.detect(mp_image)

    alert = ""

    if detection_result.detections:
        for detection in detection_result.detections:
            bbox = detection.bounding_box
            x = bbox.origin_x
            y = bbox.origin_y
            width = bbox.width
            height = bbox.height

            cv2.rectangle(img, (x, y), (x+width, y+height), (0,255,0), 2)

            face_center = x + width / 2
            frame_center = w / 2

            if face_center < frame_center - 80:
                alert = "Looking Left"
            elif face_center > frame_center + 80:
                alert = "Looking Right"
            else:
                alert = "Looking Forward"
    else:
        alert = "No Face Detected"

    cv2.putText(img, alert, (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

demo = gr.Interface(
    fn=process_frame,
    inputs=gr.Image(source="webcam", streaming=True),
    outputs="image",
    live=True
)

demo.launch()
