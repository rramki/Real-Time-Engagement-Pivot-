import streamlit as st
import cv2
import numpy as np
import mediapipe as mp

st.set_page_config(layout="wide")
st.title("🎓 AI Virtual Proctor - Face & Gaze Monitor")

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=2,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Webcam
run = st.checkbox("Start Monitoring")
FRAME_WINDOW = st.image([])

camera = cv2.VideoCapture(0)

while run:
    success, frame = camera.read()
    if not success:
        st.error("Camera not accessible")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    alert = ""

    if results.multi_face_landmarks:
        if len(results.multi_face_landmarks) > 1:
            alert = "⚠ Multiple Faces Detected"

        for face_landmarks in results.multi_face_landmarks:

            # Nose landmark
            nose = face_landmarks.landmark[1]

            h, w, _ = frame.shape
            nose_x = int(nose.x * w)

            # Looking left or right threshold
            if nose.x < 0.35:
                alert = "⚠ Looking Left"
            elif nose.x > 0.65:
                alert = "⚠ Looking Right"

    else:
        alert = "⚠ No Face Detected"

    if alert:
        cv2.putText(frame, alert, (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

    FRAME_WINDOW.image(frame, channels="BGR")
