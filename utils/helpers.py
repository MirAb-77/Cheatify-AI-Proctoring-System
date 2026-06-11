import streamlit as st
import datetime
import random
import numpy as np
import pandas as pd

# ── Colour palette ──────────────────────────────────────────────────────────
PRIMARY   = "#4F46E5"
SECONDARY = "#7C3AED"
ACCENT    = "#06B6D4"
SUCCESS   = "#22C55E"
WARNING   = "#F59E0B"
DANGER    = "#EF4444"
BG        = "#F8FAFC"
TEXT      = "#0F172A"

# ── Session-state initialiser ───────────────────────────────────────────────
def init_session_state():
    defaults = {
        "page": "landing",
        "session_active": False,
        "session_start": None,
        "calibrated_angles": None,
        "calibration_done": False,
        "gaze_direction": "Looking Center",
        "head_direction": "Looking at Screen",
        "mobile_detected": False,
        "mobile_confidence": 0.0,
        "risk_score": 0,
        "alert_count": 0,
        "events": [],
        "evidence": [],
        # stats
        "gaze_counts": {"Looking Center": 0, "Looking Left": 0,
                        "Looking Right": 0, "Looking Up": 0, "Looking Down": 0},
        "head_counts": {"Looking at Screen": 0, "Looking Left": 0,
                        "Looking Right": 0, "Looking Up": 0, "Looking Down": 0, "Tilted": 0},
        "mobile_count": 0,
        "risk_history": [],
        "risk_timestamps": [],
        # timers for screenshot logic
        "head_alarm_start": None,
        "eye_alarm_start": None,
        "mobile_alarm_start": None,
        "students_monitored": 1,
        "session_id": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ── Risk score calculation ───────────────────────────────────────────────────
def compute_risk_score(gaze, head, mobile):
    score = 0
    if gaze != "Looking Center":
        score += 25
    if head not in ("Looking at Screen",):
        score += 30
    if mobile:
        score += 45
    return min(score, 100)

def risk_level(score):
    if score == 0:   return "Clear",  SUCCESS,  "✅"
    if score < 30:   return "Low",    SUCCESS,  "🟢"
    if score < 60:   return "Medium", WARNING,  "🟡"
    if score < 80:   return "High",   DANGER,   "🔴"
    return            "Critical", DANGER,   "🚨"

# ── Event helpers ────────────────────────────────────────────────────────────
def add_event(message: str, level: str = "info"):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.events.append({
        "time": ts, "message": message, "level": level
    })

def add_evidence(frame_bytes: bytes, det_type: str, confidence: float = 1.0):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.evidence.append({
        "image": frame_bytes,
        "timestamp": ts,
        "type": det_type,
        "confidence": confidence,
    })

# ── Generate demo analytics data ─────────────────────────────────────────────
def generate_demo_timeline(n=40):
    now = datetime.datetime.now()
    times = [now - datetime.timedelta(seconds=i*15) for i in range(n)][::-1]
    events = []
    choices = [
        ("Looking Left",  "warning"),
        ("Looking Right", "warning"),
        ("Phone Detected","danger"),
        ("Head Turned",   "warning"),
        ("Normal",        "success"),
        ("Looking Down",  "warning"),
    ]
    for t in times:
        msg, lvl = random.choice(choices)
        events.append({"time": t.strftime("%H:%M:%S"), "message": msg, "level": lvl})
    return events

def get_analytics_df():
    gaze_c = st.session_state.gaze_counts
    head_c = st.session_state.head_counts
    total_frames = max(sum(gaze_c.values()), 1)

    gaze_df = pd.DataFrame([
        {"Category": k, "Count": v, "Percentage": round(v/total_frames*100,1)}
        for k, v in gaze_c.items()
    ])
    head_df = pd.DataFrame([
        {"Category": k, "Count": v, "Percentage": round(v/max(sum(head_c.values()),1)*100,1)}
        for k, v in head_c.items()
    ])
    # Risk history
    if st.session_state.risk_history:
        risk_df = pd.DataFrame({
            "Time": st.session_state.risk_timestamps,
            "Risk Score": st.session_state.risk_history,
        })
    else:
        risk_df = pd.DataFrame({"Time": [], "Risk Score": []})

    return gaze_df, head_df, risk_df

# ── Format duration ──────────────────────────────────────────────────────────
def format_duration(start: datetime.datetime) -> str:
    if start is None:
        return "00:00"
    delta = datetime.datetime.now() - start
    mins  = int(delta.total_seconds() // 60)
    secs  = int(delta.total_seconds() % 60)
    return f"{mins:02d}:{secs:02d}"

# ── HTML helpers ─────────────────────────────────────────────────────────────
def metric_card_html(icon, label, value, color, delta=None, delta_ok=True):
    delta_html = ""
    if delta:
        arrow = "↑" if not delta_ok else "↓"
        col   = DANGER if not delta_ok else SUCCESS
        delta_html = f'<div class="metric-delta" style="color:{col}">{arrow} {delta}</div>'
    return f"""
    <div class="metric-card">
      <div class="icon-wrap" style="background:linear-gradient(135deg,{color}22,{color}44)">
        <span style="font-size:22px">{icon}</span>
      </div>
      <div class="metric-value" style="color:{color}">{value}</div>
      <div class="metric-label">{label}</div>
      {delta_html}
    </div>
    """

def status_badge(text, level="info"):
    classes = {"info":"badge-info","success":"badge-success","warning":"badge-warning","danger":"badge-danger","purple":"badge-purple"}
    cls = classes.get(level, "badge-info")
    return f'<span class="badge {cls}">{text}</span>'

def detection_card_html(title, status, icon, color, extra=""):
    card_class = ""
    if color == DANGER:   card_class = "alert-active"
    elif color == WARNING: card_class = "warning-active"
    return f"""
    <div class="detection-card {card_class}">
      <div class="card-title">{title}</div>
      <div class="card-status" style="color:{color}">{icon} {status}</div>
      {extra}
    </div>
    """

def timeline_item_html(time_str, message, level):
    colors = {"danger": DANGER, "warning": WARNING, "success": SUCCESS, "info": ACCENT}
    col = colors.get(level, ACCENT)
    return f"""
    <div class="timeline-item">
      <div class="timeline-dot" style="background:{col};box-shadow:0 0 0 3px {col}22"></div>
      <div class="timeline-time">{time_str}</div>
      <div class="timeline-msg">{message}</div>
    </div>
    """
