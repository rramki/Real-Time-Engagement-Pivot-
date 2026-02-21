import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import mediapipe as mp

st.title("🎓 Real-Time AI Virtual Proctor")

# MediaPipe Setup
mp_face = mp.solutions.face_detection
mp_pose = mp.solutions.pose

face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

class ProctorProcessor(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        h, w, _ = img.shape

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Face Detection
        face_results = face_detection.process(rgb)
        pose_results = pose.process(rgb)

        alert = ""

        # ---- FACE PRESENCE ----
        if face_results.detections:
            for detection in face_results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                cv2.rectangle(img, (x, y), (x+width, y+height), (0,255,0), 2)

                # Looking direction (simple horizontal shift)
                face_center = x + width / 2
                frame_center = w / 2

                if face_center < frame_center - 80:
                    alert = "⚠ Looking Left"
                elif face_center > frame_center + 80:
                    alert = "⚠ Looking Right"
                else:
                    alert = "✅ Looking Forward"
        else:
            alert = "⚠ No Face Detected"

        # ---- POSTURE DETECTION ----
        if pose_results.pose_landmarks:
            nose = pose_results.pose_landmarks.landmark[0]
            left_shoulder = pose_results.pose_landmarks.landmark[11]
            right_shoulder = pose_results.pose_landmarks.landmark[12]

            # Check leaning forward/back (nose relative to shoulders)
            if nose.z < left_shoulder.z - 0.2:
                alert += " | ⚠ Leaning Forward"

        if alert:
            cv2.putText(img, alert, (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255), 2)

        return img

webrtc_streamer(key="proctor", video_processor_factory=ProctorProcessor)
