import cv2
import streamlit as st
import numpy as np


from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # nano version

results = model(frame)

for r in results:
    for box in r.boxes:
        cls = int(box.cls[0])
        if model.names[cls] == "cell phone":
            st.error("Mobile Phone Detected!")

import sounddevice as sd
import numpy as np

duration = 3
audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
sd.wait()

volume_norm = np.linalg.norm(audio) * 10

if volume_norm < 1:
    print("Silence detected")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

st.markdown("""
<script>
document.addEventListener("visibilitychange", function() {
    if (document.hidden) {
        alert("Tab switched!");
    }
});
</script>
""", unsafe_allow_html=True)

st.title("Simple Virtual Proctor")

run = st.checkbox("Start Monitoring")

FRAME_WINDOW = st.image([])

camera = cv2.VideoCapture(0)

while run:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        st.warning("No Face Detected!")

    if len(faces) > 1:
        st.error("Multiple Faces Detected!")

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    FRAME_WINDOW.image(frame, channels="BGR")
