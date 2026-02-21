import gradio as gr
import cv2
import numpy as np
import librosa
import torch
from transformers import pipeline

# Load emotion model (CPU)
emotion_model = pipeline(
    "image-classification",
    model="dima806/facial_emotions_image_detection",
    device=-1
)

# Engagement scoring logic
def calculate_engagement(emotion, silence_ratio):
    score = 0

    if emotion in ["happy", "surprise"]:
        score += 50
    elif emotion in ["neutral"]:
        score += 30
    else:
        score += 10

    if silence_ratio < 0.3:
        score += 50
    elif silence_ratio < 0.6:
        score += 30
    else:
        score += 10

    return score

def suggest_intervention(score):
    if score < 40:
        return "⚠ Low engagement detected. Try asking a question or introducing interactive content."
    elif score < 70:
        return "Moderate engagement. Consider changing tone or showing visuals."
    else:
        return "Good engagement level 👍"

# Audio silence detection
def analyze_audio(audio):
    if audio is None:
        return 1.0

    y, sr = librosa.load(audio, sr=None)
    energy = np.mean(librosa.feature.rms(y=y))
    silence_ratio = 1 - min(energy * 100, 1)
    return silence_ratio

# Video emotion detection
def analyze_video(frame):
    if frame is None:
        return "neutral"

    frame = cv2.resize(frame, (224, 224))  # reduce memory
    results = emotion_model(frame)
    return results[0]["label"].lower()

# Main processing function
def analyze_engagement(video_frame, audio_file):
    emotion = analyze_video(video_frame)
    silence_ratio = analyze_audio(audio_file)

    score = calculate_engagement(emotion, silence_ratio)
    suggestion = suggest_intervention(score)

    return f"Emotion: {emotion}", score, suggestion

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🎯 Real-Time Engagement Detection System")

    with gr.Row():
        video = gr.Image(source="webcam", streaming=True)
        audio = gr.Audio(source="microphone", type="filepath")

    emotion_output = gr.Textbox(label="Detected Emotion")
    engagement_score = gr.Number(label="Engagement Score")
    suggestion_output = gr.Textbox(label="Suggested Intervention")

    analyze_btn = gr.Button("Analyze Engagement")

    analyze_btn.click(
        analyze_engagement,
        inputs=[video, audio],
        outputs=[emotion_output, engagement_score, suggestion_output]
    )

demo.launch()
