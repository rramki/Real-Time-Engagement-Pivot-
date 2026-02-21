import streamlit as st
import cv2
import numpy as np

st.set_page_config(layout="wide")
st.title("🎓 Cloud AI Virtual Proctor")

# Load Haar cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

image_file = st.camera_input("Take a photo")

if image_file is not None:
    # Convert to OpenCV format
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    alert = ""

    if len(faces) == 0:
        alert = "⚠ No Face Detected"

    elif len(faces) > 1:
        alert = "⚠ Multiple Faces Detected"

    else:
        (x, y, w, h) = faces[0]

        frame_center = frame.shape[1] / 2
        face_center = x + w / 2

        if face_center < frame_center - 80:
            alert = "⚠ Looking Left"
        elif face_center > frame_center + 80:
            alert = "⚠ Looking Right"
        else:
            alert = "✅ Looking Forward"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

    st.image(frame, channels="BGR")

    if alert:
        st.subheader(alert)
