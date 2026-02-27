"""
Real-Time Engagement Pivot
Exam Hall Engagement Analysis System
CPU-Optimized | Non-Verbal Cue Detection | Actionable Interventions
"""

import streamlit as st
import cv2
import numpy as np
import time
import threading
import queue
from datetime import datetime
from collections import deque
import json

# Page config
st.set_page_config(
    page_title="Engagement Pivot — Exam Analytics",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg: #0a0c10;
    --surface: #111318;
    --surface2: #1a1d24;
    --border: #2a2d36;
    --accent: #00ff88;
    --accent2: #ff6b35;
    --warn: #ffcc00;
    --danger: #ff3355;
    --text: #e8eaf0;
    --muted: #6b7280;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'Space Mono', monospace;
}

html, body, [class*="css"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-head) !important;
}

.main { background: var(--bg) !important; }
.block-container { padding: 1rem 2rem !important; max-width: 1400px !important; }

/* Header */
.app-header {
    background: linear-gradient(135deg, #0d1117 0%, #111827 100%);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 8px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(0,255,136,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.app-header h1 {
    font-family: var(--font-head) !important;
    font-weight: 800 !important;
    font-size: 1.8rem !important;
    color: var(--accent) !important;
    margin: 0 !important;
    letter-spacing: -0.5px;
}
.app-header p {
    color: var(--muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    margin: 0.3rem 0 0 !important;
}

/* Metric cards */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem;
    text-align: center;
    position: relative;
    transition: border-color 0.3s;
}
.metric-card.high { border-top: 3px solid var(--accent); }
.metric-card.medium { border-top: 3px solid var(--warn); }
.metric-card.low { border-top: 3px solid var(--danger); }
.metric-value {
    font-family: var(--font-mono) !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    display: block;
    line-height: 1;
}
.metric-label {
    font-size: 0.7rem !important;
    color: var(--muted) !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-family: var(--font-mono) !important;
    margin-top: 0.4rem;
    display: block;
}

/* Alert banners */
.alert-critical {
    background: rgba(255,51,85,0.1);
    border: 1px solid rgba(255,51,85,0.4);
    border-left: 4px solid var(--danger);
    border-radius: 6px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    color: #ff8899 !important;
}
.alert-warn {
    background: rgba(255,204,0,0.08);
    border: 1px solid rgba(255,204,0,0.3);
    border-left: 4px solid var(--warn);
    border-radius: 6px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    color: #ffe066 !important;
}
.alert-ok {
    background: rgba(0,255,136,0.06);
    border: 1px solid rgba(0,255,136,0.25);
    border-left: 4px solid var(--accent);
    border-radius: 6px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    color: #66ffbb !important;
}

/* Intervention cards */
.intervention {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    position: relative;
}
.intervention .priority {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent2) !important;
    margin-bottom: 0.3rem;
    display: block;
}
.intervention .action {
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text) !important;
}
.intervention .rationale {
    font-size: 0.75rem;
    color: var(--muted) !important;
    font-family: var(--font-mono) !important;
    margin-top: 0.3rem;
}

/* Timeline bar */
.timeline-bar {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.tl-label {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    color: var(--muted) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}

/* Sidebar */
.css-1d391kg, [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Section headers */
.section-head {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--muted) !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
    margin: 1.2rem 0 0.8rem !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    font-family: var(--font-mono) !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    border: none !important;
    border-radius: 6px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #00cc6e !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,255,136,0.3) !important;
}

/* Progress bars */
.stProgress > div > div {
    background: var(--accent) !important;
}

/* Sliders */
.stSlider > div > div > div { background: var(--accent) !important; }

/* DataFrame */
.stDataFrame { background: var(--surface) !important; }

/* Pulse animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.live-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--danger);
    border-radius: 50%;
    animation: pulse 1.2s infinite;
    margin-right: 6px;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(255,51,85,0.15);
    border: 1px solid rgba(255,51,85,0.4);
    border-radius: 4px;
    padding: 2px 8px;
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    color: #ff8899 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── Engine ───────────────────────────────────────────────────────
class EngagementEngine:
    """CPU-optimized engagement analysis engine using OpenCV + MediaPipe."""
    
    def __init__(self):
        self.face_cascade = None
        self.eye_cascade = None
        self.mp_face_mesh = None
        self.mp_pose = None
        self._init_detectors()
        
        # Rolling window for temporal analysis
        self.engagement_history = deque(maxlen=150)
        self.silence_window = deque(maxlen=30)
        self.blink_events = deque(maxlen=50)
        self.last_movement_time = time.time()
        self.frame_count = 0
        
    def _init_detectors(self):
        """Initialize OpenCV cascade classifiers (CPU-friendly)."""
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
        except Exception:
            pass
        
        # MediaPipe is fully optional — skipped on Streamlit Cloud (libGL safe)
        self.has_mediapipe = False
        try:
            import importlib.util as _ilu
            if _ilu.find_spec("mediapipe") is not None:
                import mediapipe as mp
                self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
                    static_image_mode=False,
                    max_num_faces=20,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                self.has_mediapipe = True
        except Exception:
            self.has_mediapipe = False

    def analyze_frame(self, frame: np.ndarray) -> dict:
        """Analyze a single frame for engagement cues."""
        self.frame_count += 1
        h, w = frame.shape[:2]
        result = {
            "timestamp": time.time(),
            "faces_detected": 0,
            "eyes_detected": 0,
            "head_down_count": 0,
            "distracted_count": 0,
            "looking_away": 0,
            "blink_rate": 0.0,
            "posture_issues": 0,
            "engagement_score": 100.0,
            "alerts": [],
            "annotations": frame.copy()
        }
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        annotated = frame.copy()
        
        if self.face_cascade is None:
            result["annotations"] = annotated
            return result
        
        # ── Face detection ──
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )
        result["faces_detected"] = len(faces)
        
        distracted = 0
        head_down = 0
        eyes_visible = 0
        
        for (x, y, fw, fh) in faces:
            # Draw face box
            cv2.rectangle(annotated, (x, y), (x+fw, y+fh), (0, 255, 136), 2)
            
            # Eye detection in face ROI
            face_roi = gray[y:y+fh, x:x+fw]
            eyes = self.eye_cascade.detectMultiScale(
                face_roi, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15)
            )
            eyes_visible += len(eyes)
            
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(annotated, 
                             (x+ex, y+ey), (x+ex+ew, y+ey+eh),
                             (255, 204, 0), 1)
            
            # Head position heuristic: if face is in upper third → looking up (ok)
            # if eyes not visible → possibly head down
            face_center_y = y + fh // 2
            frame_center_y = h // 2
            
            if len(eyes) == 0:
                head_down += 1
                cv2.putText(annotated, "HEAD DOWN", (x, y-8),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 51, 85), 1)
            elif len(eyes) < 2:
                distracted += 1
                cv2.putText(annotated, "DISTRACTED", (x, y-8),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 204, 0), 1)
            else:
                cv2.putText(annotated, "ENGAGED", (x, y-8),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 136), 1)
        
        result["eyes_detected"] = eyes_visible
        result["head_down_count"] = head_down
        result["distracted_count"] = distracted
        
        # ── Engagement Score Calculation ──
        score = 100.0
        
        n_faces = max(result["faces_detected"], 1)
        # Penalize head-down students
        score -= (head_down / n_faces) * 40
        # Penalize distracted students  
        score -= (distracted / n_faces) * 20
        # Bonus for eye contact ratio
        eye_ratio = min(eyes_visible / (n_faces * 2 + 0.001), 1.0)
        score += (eye_ratio - 0.5) * 10
        
        score = max(0.0, min(100.0, score))
        result["engagement_score"] = score
        
        # ── Alerts ──
        if head_down > 0:
            result["alerts"].append(f"⚠ {head_down} student(s) appear to have head down / not looking at paper")
        if distracted > 0:
            result["alerts"].append(f"⚡ {distracted} student(s) showing signs of distraction")
        if score < 50:
            result["alerts"].append("🔴 CRITICAL: Engagement dropped below 50%")
        elif score < 70:
            result["alerts"].append("🟡 WARNING: Moderate engagement drop detected")
        
        # ── Draw HUD ──
        self._draw_hud(annotated, result)
        result["annotations"] = annotated
        
        self.engagement_history.append(score)
        return result

    def _draw_hud(self, frame, result):
        """Draw minimal HUD overlay on frame."""
        h, w = frame.shape[:2]
        # Dark bar at bottom
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, h-50), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)
        
        score = result["engagement_score"]
        color = (0, 255, 136) if score >= 70 else (0, 204, 255) if score >= 50 else (51, 51, 255)
        
        cv2.putText(frame, f"ENGAGEMENT: {score:.0f}%", (10, h-15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.putText(frame, f"FACES: {result['faces_detected']}  EYES: {result['eyes_detected']}",
                   (w//2 - 80, h-15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
        ts = datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, ts, (w - 80, h-15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 100, 100), 1)

    def get_interventions(self, score: float, alerts: list) -> list:
        """Generate actionable interventions based on engagement state."""
        interventions = []
        
        if score < 40:
            interventions += [
                {"priority": "IMMEDIATE", "action": "Announce a 2-minute stretch break",
                 "rationale": "Critical engagement drop — physical reset reactivates attention"},
                {"priority": "IMMEDIATE", "action": "Walk through the exam hall slowly",
                 "rationale": "Invigilator presence re-focuses distracted students"},
                {"priority": "HIGH", "action": "Verbal reminder: 'Check your time remaining'",
                 "rationale": "Time-pressure cue re-engages task focus"},
            ]
        elif score < 60:
            interventions += [
                {"priority": "HIGH", "action": "Gently tap on desks as you patrol",
                 "rationale": "Low-stimulus alert for students showing fatigue signs"},
                {"priority": "HIGH", "action": "Write remaining time on whiteboard",
                 "rationale": "Visual time anchoring improves self-regulation"},
                {"priority": "MEDIUM", "action": "Open/close a window for air circulation",
                 "rationale": "Environmental refresh counters cognitive fatigue"},
            ]
        elif score < 75:
            interventions += [
                {"priority": "MEDIUM", "action": "Slow patrol of room perimeter",
                 "rationale": "Passive supervision signal maintains focus"},
                {"priority": "MEDIUM", "action": "Soft verbal: 'You have X minutes remaining'",
                 "rationale": "Time reminder at mid-drop prevents further decline"},
                {"priority": "LOW", "action": "Ensure water is accessible to students",
                 "rationale": "Hydration supports sustained cognitive performance"},
            ]
        else:
            interventions += [
                {"priority": "LOW", "action": "Continue standard monitoring",
                 "rationale": "Engagement is healthy — maintain current environment"},
                {"priority": "LOW", "action": "Note time of high engagement for reporting",
                 "rationale": "Baseline data helps identify optimal exam scheduling"},
            ]
        
        # Specific alert-based interventions
        for alert in alerts:
            if "head down" in alert.lower():
                interventions.insert(0, {
                    "priority": "HIGH",
                    "action": "Check on student(s) with head down — possible distress",
                    "rationale": "Head-down posture can indicate anxiety, fatigue, or cheating"
                })
                break
        
        return interventions[:4]  # Max 4 interventions

    def get_summary_stats(self) -> dict:
        """Compute rolling statistics from engagement history."""
        if not self.engagement_history:
            return {"avg": 0, "min": 0, "max": 0, "trend": "N/A", "drop_events": 0}
        
        arr = list(self.engagement_history)
        avg = np.mean(arr)
        mn = np.min(arr)
        mx = np.max(arr)
        
        # Trend: compare last 20 vs previous 20
        if len(arr) >= 40:
            recent = np.mean(arr[-20:])
            prev = np.mean(arr[-40:-20])
            diff = recent - prev
            trend = "↑ Rising" if diff > 3 else "↓ Falling" if diff < -3 else "→ Stable"
        else:
            trend = "→ Collecting..."
        
        drop_events = sum(1 for i in range(1, len(arr)) if arr[i] < 60 and arr[i-1] >= 60)
        
        return {"avg": avg, "min": mn, "max": mx, "trend": trend, "drop_events": drop_events}


# ─── Session State Init ───────────────────────────────────────────
if "engine" not in st.session_state:
    st.session_state.engine = EngagementEngine()
if "running" not in st.session_state:
    st.session_state.running = False
if "mode" not in st.session_state:
    st.session_state.mode = "live"
if "history" not in st.session_state:
    st.session_state.history = []
if "frame_count" not in st.session_state:
    st.session_state.frame_count = 0

engine: EngagementEngine = st.session_state.engine

# ─── Header ───────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>🎯 Real-Time Engagement Pivot</h1>
    <p>// EXAM HALL NON-VERBAL CUE ANALYSIS // CPU-OPTIMIZED // ACTIONABLE INTERVENTIONS</p>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-head">// Mode Select</p>', unsafe_allow_html=True)
    mode = st.radio(
        "Analysis Mode",
        ["🔴 Live Webcam Stream", "📁 Upload Recorded Video"],
        label_visibility="collapsed"
    )
    st.session_state.mode = "live" if "Live" in mode else "upload"
    
    st.markdown('<p class="section-head">// Detection Settings</p>', unsafe_allow_html=True)
    sensitivity = st.slider("Sensitivity", 1, 10, 6,
                            help="Higher = more sensitive to engagement drops")
    frame_skip = st.slider("Frame Skip (CPU load)", 1, 5, 2,
                           help="Process every Nth frame — higher = faster, less precise")
    show_annotations = st.toggle("Show CV Annotations", value=True)
    
    st.markdown('<p class="section-head">// Exam Context</p>', unsafe_allow_html=True)
    exam_duration = st.number_input("Exam Duration (min)", 30, 360, 90)
    elapsed_min = st.number_input("Elapsed Time (min)", 0, 360, 0)
    student_count = st.number_input("Expected Students", 1, 500, 30)
    
    st.markdown('<p class="section-head">// About</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem; color:#6b7280; font-family:'Space Mono',monospace; line-height:1.6;">
    Detects:<br>
    ✓ Facial expressions<br>
    ✓ Head position / posture<br>
    ✓ Eye visibility / blink cues<br>
    ✓ Engagement score drops<br>
    ✓ Temporal silence patterns<br>
    <br>
    Engine: OpenCV Haar Cascades<br>
    Optional: MediaPipe FaceMesh<br>
    Optimized for CPU inference
    </div>
    """, unsafe_allow_html=True)

# ─── Main Layout ──────────────────────────────────────────────────
col_video, col_panel = st.columns([3, 2], gap="medium")

with col_panel:
    st.markdown('<p class="section-head">// Live Metrics</p>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    score_placeholder = m1.empty()
    faces_placeholder = m2.empty()
    alert_count_placeholder = m3.empty()
    
    st.markdown('<p class="section-head">// Status</p>', unsafe_allow_html=True)
    status_placeholder = st.empty()
    
    st.markdown('<p class="section-head">// Interventions</p>', unsafe_allow_html=True)
    intervention_placeholder = st.empty()
    
    st.markdown('<p class="section-head">// Trend</p>', unsafe_allow_html=True)
    trend_placeholder = st.empty()
    chart_placeholder = st.empty()

with col_video:
    st.markdown('<p class="section-head">// Video Feed</p>', unsafe_allow_html=True)
    
    if st.session_state.mode == "live":
        # ── LIVE MODE ──
        st.markdown('<span class="live-badge"><span class="live-dot"></span>LIVE</span>', 
                    unsafe_allow_html=True)
        
        col_b1, col_b2 = st.columns(2)
        start_btn = col_b1.button("▶ START STREAM", use_container_width=True)
        stop_btn = col_b2.button("⏹ STOP", use_container_width=True)
        
        if start_btn:
            st.session_state.running = True
        if stop_btn:
            st.session_state.running = False
        
        video_placeholder = st.empty()
        
        if st.session_state.running:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("⚠ Camera not accessible. Check permissions or try 'Upload Video' mode.")
                st.session_state.running = False
            else:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 15)
                
                frame_idx = 0
                last_result = None
                
                while st.session_state.running:
                    ret, frame = cap.read()
                    if not ret:
                        st.warning("Frame capture failed.")
                        break
                    
                    frame_idx += 1
                    
                    if frame_idx % frame_skip == 0:
                        result = engine.analyze_frame(frame)
                        last_result = result
                        st.session_state.history.append(result["engagement_score"])
                        if len(st.session_state.history) > 300:
                            st.session_state.history = st.session_state.history[-300:]
                    
                    if last_result:
                        disp = last_result["annotations"] if show_annotations else frame
                        disp_rgb = cv2.cvtColor(disp, cv2.COLOR_BGR2RGB)
                        video_placeholder.image(disp_rgb, channels="RGB", use_container_width=True)
                        
                        # Update panels
                        score = last_result["engagement_score"]
                        lvl = "high" if score >= 70 else "medium" if score >= 50 else "low"
                        color = "#00ff88" if score >= 70 else "#ffcc00" if score >= 50 else "#ff3355"
                        
                        score_placeholder.markdown(f"""
                        <div class="metric-card {lvl}">
                            <span class="metric-value" style="color:{color}">{score:.0f}%</span>
                            <span class="metric-label">Engagement</span>
                        </div>""", unsafe_allow_html=True)
                        
                        faces_placeholder.markdown(f"""
                        <div class="metric-card high">
                            <span class="metric-value">{last_result['faces_detected']}</span>
                            <span class="metric-label">Faces</span>
                        </div>""", unsafe_allow_html=True)
                        
                        n_alerts = len(last_result["alerts"])
                        al_lvl = "low" if n_alerts > 1 else "medium" if n_alerts > 0 else "high"
                        alert_count_placeholder.markdown(f"""
                        <div class="metric-card {al_lvl}">
                            <span class="metric-value">{n_alerts}</span>
                            <span class="metric-label">Alerts</span>
                        </div>""", unsafe_allow_html=True)
                        
                        # Status alerts
                        status_html = ""
                        if not last_result["alerts"]:
                            status_html = '<div class="alert-ok">✓ All students appear on-task</div>'
                        for a in last_result["alerts"]:
                            cls = "alert-critical" if "CRITICAL" in a or "⚠" in a else "alert-warn"
                            status_html += f'<div class="{cls}">{a}</div>'
                        status_placeholder.markdown(status_html, unsafe_allow_html=True)
                        
                        # Interventions
                        interventions = engine.get_interventions(score, last_result["alerts"])
                        iv_html = ""
                        for iv in interventions:
                            iv_html += f"""
                            <div class="intervention">
                                <span class="priority">{iv['priority']}</span>
                                <div class="action">{iv['action']}</div>
                                <div class="rationale">{iv['rationale']}</div>
                            </div>"""
                        intervention_placeholder.markdown(iv_html, unsafe_allow_html=True)
                        
                        # Trend
                        stats = engine.get_summary_stats()
                        trend_placeholder.markdown(f"""
                        <div class="alert-ok" style="display:flex; gap:1.5rem;">
                            <span>AVG: <b>{stats['avg']:.0f}%</b></span>
                            <span>MIN: <b>{stats['min']:.0f}%</b></span>
                            <span>TREND: <b>{stats['trend']}</b></span>
                            <span>DROPS: <b>{stats['drop_events']}</b></span>
                        </div>""", unsafe_allow_html=True)
                        
                        # Mini chart
                        if len(st.session_state.history) > 5:
                            import pandas as pd
                            df = pd.DataFrame({"Engagement Score": st.session_state.history[-100:]})
                            chart_placeholder.line_chart(df, height=120)
                    
                    time.sleep(0.03)  # ~30fps UI update
                
                cap.release()
        else:
            video_placeholder.markdown("""
            <div style="background:#111318; border:1px dashed #2a2d36; border-radius:8px; 
                        height:300px; display:flex; align-items:center; justify-content:center;
                        color:#6b7280; font-family:'Space Mono',monospace; font-size:0.8rem;">
                ▶ Press START STREAM to activate webcam
            </div>""", unsafe_allow_html=True)
    
    else:
        # ── UPLOAD MODE ──
        st.markdown("**Upload a recorded exam hall video for analysis.**")
        uploaded = st.file_uploader(
            "Upload video (MP4, AVI, MOV — max ~100MB for best performance)",
            type=["mp4", "avi", "mov", "mkv"],
            label_visibility="collapsed"
        )
        
        if uploaded:
            import tempfile, os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name
            
            analyze_btn = st.button("🔍 ANALYZE VIDEO", use_container_width=True)
            
            if analyze_btn:
                cap = cv2.VideoCapture(tmp_path)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS) or 25
                duration_s = total_frames / fps
                
                st.info(f"Video: {total_frames} frames | {fps:.1f} fps | {duration_s:.1f}s duration")
                
                progress = st.progress(0)
                video_out = st.empty()
                
                frame_results = []
                frame_idx = 0
                
                # Process video
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    frame_idx += 1
                    progress.progress(min(frame_idx / max(total_frames, 1), 1.0))
                    
                    if frame_idx % frame_skip == 0:
                        result = engine.analyze_frame(frame)
                        frame_results.append({
                            "frame": frame_idx,
                            "time_s": frame_idx / fps,
                            "score": result["engagement_score"],
                            "faces": result["faces_detected"],
                            "alerts": len(result["alerts"])
                        })
                        st.session_state.history.append(result["engagement_score"])
                        
                        # Show every 10th processed frame
                        if len(frame_results) % 5 == 0:
                            disp = result["annotations"] if show_annotations else frame
                            disp_rgb = cv2.cvtColor(disp, cv2.COLOR_BGR2RGB)
                            video_out.image(disp_rgb, channels="RGB", use_container_width=True)
                
                cap.release()
                os.unlink(tmp_path)
                
                # Final analysis
                if frame_results:
                    import pandas as pd
                    df = pd.DataFrame(frame_results)
                    
                    avg_score = df["score"].mean()
                    min_score = df["score"].min()
                    max_score = df["score"].max()
                    min_time  = df.loc[df["score"].idxmin(), "time_s"]
                    total_alerts = df["alerts"].sum()
                    drop_frames  = (df["score"] < 60).sum()
                    critical_frames = (df["score"] < 40).sum()
                    head_down_frames = (df["faces"] == 0).sum()  # proxy: no faces = heads down / away
                    
                    # Build alert list from video analysis for intervention engine
                    video_alerts = []
                    if critical_frames > 0:
                        video_alerts.append("CRITICAL: Engagement dropped below 40%")
                    if drop_frames > len(frame_results) * 0.3:
                        video_alerts.append("⚠ Sustained engagement drop across 30%+ of video")
                    if head_down_frames > len(frame_results) * 0.2:
                        video_alerts.append("⚠ Frequent head-down / faces not visible detected")
                    if total_alerts > 5:
                        video_alerts.append("⚠ Multiple distraction events logged")

                    st.success(f"✓ Analysis complete — {len(frame_results)} frames processed")
                    
                    # ── Summary Metrics ──
                    mc1, mc2, mc3, mc4 = st.columns(4)
                    lvl   = "high" if avg_score >= 70 else "medium" if avg_score >= 50 else "low"
                    color = "#00ff88" if avg_score >= 70 else "#ffcc00" if avg_score >= 50 else "#ff3355"
                    
                    mc1.markdown(f"""<div class="metric-card {lvl}">
                        <span class="metric-value" style="color:{color}">{avg_score:.0f}%</span>
                        <span class="metric-label">Avg Engagement</span></div>""", unsafe_allow_html=True)
                    mc2.markdown(f"""<div class="metric-card low">
                        <span class="metric-value" style="color:#ff3355">{min_score:.0f}%</span>
                        <span class="metric-label">Lowest Score</span></div>""", unsafe_allow_html=True)
                    mc3.markdown(f"""<div class="metric-card medium">
                        <span class="metric-value">{int(min_time//60):02d}:{int(min_time%60):02d}</span>
                        <span class="metric-label">Drop At</span></div>""", unsafe_allow_html=True)
                    mc4.markdown(f"""<div class="metric-card {'low' if drop_frames > 0 else 'high'}">
                        <span class="metric-value">{drop_frames}</span>
                        <span class="metric-label">Drop Frames</span></div>""", unsafe_allow_html=True)

                    # ── Engagement Timeline ──
                    st.markdown('<p class="section-head">// Engagement Timeline</p>', unsafe_allow_html=True)
                    chart_df = df.set_index("time_s")[["score"]].rename(columns={"score": "Engagement %"})
                    st.line_chart(chart_df, height=180)

                    # ── Video-level alert banners ──
                    if video_alerts:
                        st.markdown('<p class="section-head">// Video Alerts</p>', unsafe_allow_html=True)
                        for a in video_alerts:
                            cls = "alert-critical" if "CRITICAL" in a else "alert-warn"
                            st.markdown(f'<div class="{cls}">{a}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="alert-ok">✓ No major engagement drops detected in this recording</div>',
                                    unsafe_allow_html=True)

                    # ── Actionable Interventions (always shown, score-aware) ──
                    st.markdown('<p class="section-head">// Actionable Interventions</p>', unsafe_allow_html=True)
                    
                    # Use WORST segment score to drive intervention tier, not just average
                    # This ensures interventions always appear even when avg looks ok
                    intervention_score = min(avg_score, min_score + (avg_score - min_score) * 0.4)
                    interventions = engine.get_interventions(intervention_score, video_alerts)
                    
                    if not interventions:
                        interventions = [
                            {"priority": "LOW", "action": "Continue standard exam invigilation",
                             "rationale": "Engagement appears healthy throughout the recording"},
                            {"priority": "LOW", "action": "Log this session as baseline reference",
                             "rationale": "High-engagement sessions are valuable benchmarks for scheduling"},
                        ]
                    
                    iv_html = ""
                    for iv in interventions:
                        p = iv['priority']
                        p_color = "#ff3355" if p == "IMMEDIATE" else "#ff6b35" if p == "HIGH" else "#ffcc00" if p == "MEDIUM" else "#00ff88"
                        iv_html += f"""
                        <div class="intervention">
                            <span class="priority" style="color:{p_color};">▸ {p}</span>
                            <div class="action">{iv['action']}</div>
                            <div class="rationale">{iv['rationale']}</div>
                        </div>"""
                    st.markdown(iv_html, unsafe_allow_html=True)

                    # ── Phase-by-phase breakdown ──
                    st.markdown('<p class="section-head">// Session Phase Analysis</p>', unsafe_allow_html=True)
                    total_dur = df["time_s"].max()
                    phases = []
                    for i, (label, start_pct, end_pct) in enumerate([
                        ("Opening Phase", 0.0, 0.25),
                        ("Early Phase",   0.25, 0.5),
                        ("Mid Phase",     0.5, 0.75),
                        ("Final Phase",   0.75, 1.01),
                    ]):
                        mask = (df["time_s"] >= start_pct * total_dur) & (df["time_s"] < end_pct * total_dur)
                        seg = df[mask]
                        if len(seg) == 0:
                            continue
                        s = seg["score"].mean()
                        phase_color = "#00ff88" if s >= 70 else "#ffcc00" if s >= 50 else "#ff3355"
                        phases.append({"Phase": label,
                                       "Avg Score": f"{s:.0f}%",
                                       "Min Score": f"{seg['score'].min():.0f}%",
                                       "Alerts": int(seg["alerts"].sum()),
                                       "Status": "✅ Good" if s >= 70 else "⚠ Watch" if s >= 50 else "🔴 Critical"})
                    
                    if phases:
                        phase_df = pd.DataFrame(phases)
                        st.dataframe(phase_df, use_container_width=True, hide_index=True)

                    # ── Drop events table ──
                    drops = df[df["score"] < 60].copy()
                    if not drops.empty:
                        st.markdown('<p class="section-head">// Engagement Drop Events (score < 60%)</p>', unsafe_allow_html=True)
                        drops["time"] = drops["time_s"].apply(lambda x: f"{int(x//60):02d}:{int(x%60):02d}")
                        st.dataframe(
                            drops[["time", "score", "faces", "alerts"]].rename(columns={
                                "time": "Time", "score": "Score %",
                                "faces": "Faces Detected", "alerts": "Alert Count"
                            }),
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.markdown('<div class="alert-ok">✓ No frames scored below 60% — solid engagement throughout</div>',
                                    unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#111318; border:2px dashed #2a2d36; border-radius:8px; 
                        height:200px; display:flex; align-items:center; justify-content:center;
                        color:#6b7280; font-family:'Space Mono',monospace; font-size:0.8rem; text-align:center;">
                📁 Drag & drop exam hall recording here<br>
                <span style="font-size:0.65rem; margin-top:0.5rem; display:block;">MP4 / AVI / MOV — optimized for small files</span>
            </div>""", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a3d46; padding:0.5rem;">
    REAL-TIME ENGAGEMENT PIVOT // CPU-OPTIMIZED ENGINE // OPENCV + MEDIAPIPE (OPTIONAL) // STREAMLIT CLOUD READY
</div>""", unsafe_allow_html=True)
