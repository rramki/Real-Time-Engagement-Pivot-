# 🎯 Real-Time Engagement Pivot
### Exam Hall Non-Verbal Cue Analysis System

A **CPU-optimized** Streamlit application that analyzes non-verbal cues (facial expressions, head posture, eye visibility) and detects engagement drops in real-time from live webcam streams or uploaded exam hall recordings — then suggests **actionable invigilator interventions**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔴 Live Stream | Real-time webcam analysis with frame-by-frame scoring |
| 📁 Video Upload | Analyze recorded exam hall MP4/AVI/MOV files |
| 👁 Face & Eye Detection | OpenCV Haar Cascade (CPU-friendly) |
| 🤔 Head Posture | Detects head-down / looking away via eye visibility |
| 📊 Engagement Score | Rolling 0–100% score with trend analysis |
| 🚨 Alert System | Critical / Warning / OK status banners |
| 💡 Interventions | Context-aware, prioritized invigilator actions |
| ⚡ MediaPipe (Optional) | Enhanced face mesh when available |

---

## 🚀 Deploy to Streamlit Cloud (Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Engagement Pivot v1"
git remote add origin https://github.com/YOUR_USERNAME/engagement-pivot.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy!**

> ⚠️ **Note on Live Webcam**: Browser webcam access works on HTTPS (Streamlit Cloud provides this). On localhost, it uses `cv2.VideoCapture(0)` directly.

---

## 💻 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

---

## 🧠 How It Works

### Non-Verbal Cue Detection Pipeline

```
Video Frame → Grayscale → Face Detection (Haar Cascade)
                ↓
          Eye Detection (per face ROI)
                ↓
    ┌─ Eyes visible (2) → ENGAGED
    ├─ Eyes partial (1) → DISTRACTED  
    └─ Eyes absent (0)  → HEAD DOWN
                ↓
    Engagement Score = f(engaged_ratio, eye_ratio)
                ↓
    Rolling Average → Trend Analysis → Alerts → Interventions
```

### Engagement Score Formula
```python
score = 100
score -= (head_down_count / total_faces) * 40   # Heavy penalty
score -= (distracted_count / total_faces) * 20  # Moderate penalty
score += (eye_ratio - 0.5) * 10                 # Bonus for eye contact
score = clamp(score, 0, 100)
```

### Intervention Tiers
| Score | Priority | Examples |
|---|---|---|
| < 40% | IMMEDIATE | Stretch break, walk the hall |
| 40–60% | HIGH | Time reminder, desk taps |
| 60–75% | MEDIUM | Patrol, open windows |
| ≥ 75% | LOW | Standard monitoring |

---

## ⚙️ Settings

| Setting | Effect |
|---|---|
| Sensitivity (1–10) | Adjusts alert thresholds |
| Frame Skip (1–5) | Skip N frames to reduce CPU load |
| Show CV Annotations | Toggle bounding boxes on/off |
| Exam Duration | Provides exam context |

---

## 📦 Dependencies

- **streamlit** — UI framework
- **opencv-python-headless** — Computer vision (no GUI, Streamlit Cloud compatible)
- **numpy / pandas** — Numerical analysis
- **mediapipe** *(optional)* — Enhanced face mesh detection
- **Pillow / scipy** — Image processing utilities

---

## 🔧 Streamlit Cloud Notes

- Use `opencv-python-headless` (not `opencv-python`) — required for cloud
- Webcam in live mode requires browser HTTPS permission prompt
- Video uploads limited to 200MB (configurable in `config.toml`)
- CPU-only: no GPU required

---

## 📁 File Structure

```
engagement-pivot/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .streamlit/
    └── config.toml           # Streamlit configuration
```

---

*Built for real-time exam hall engagement monitoring. CPU-optimized for deployment on Streamlit Community Cloud.*
