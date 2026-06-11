import streamlit as st
import cv2
import numpy as np
import time
import datetime
import os
import sys

# Add parent dir so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
from utils.helpers import (
    PRIMARY, SECONDARY, ACCENT, SUCCESS, WARNING, DANGER,
    compute_risk_score, risk_level, add_event, add_evidence,
    detection_card_html, timeline_item_html, format_duration
)

EVIDENCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "evidence_gallery")
os.makedirs(EVIDENCE_DIR, exist_ok=True)


def render_monitoring():
    st.markdown('<div class="page-title">Live Monitoring</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-breadcrumb">Real-time detection • All three modules active</div>',
                unsafe_allow_html=True)

    # ── Session controls ─────────────────────────────────────────────────────
    ctrl_col, _, info_col = st.columns([2, 1, 2])
    with ctrl_col:
        if not st.session_state.session_active:
            if st.button("▶  Start Session", use_container_width=True):
                st.session_state.session_active = True
                st.session_state.session_start  = datetime.datetime.now()
                st.session_state.calibration_done = False
                st.session_state.calibrated_angles = None
                st.session_state.session_id = f"PRK-{int(time.time()) % 100000}"
                add_event("Session started — calibrating head pose (5s)", "info")
                st.rerun()
        else:
            if st.button("⏹  End Session", use_container_width=True):
                st.session_state.session_active = False
                add_event("Session ended by invigilator", "info")
                st.rerun()

    with info_col:
        if st.session_state.session_active:
            dur = format_duration(st.session_state.session_start)
            st.markdown(f"""
            <div style="display:flex;gap:16px;align-items:center;justify-content:flex-end">
              <div style="text-align:center">
                <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:800;
                     color:{PRIMARY}">{dur}</div>
                <div style="font-size:11px;color:#64748B">Duration</div>
              </div>
              <div style="text-align:center">
                <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:800;
                     color:{DANGER}">{st.session_state.alert_count}</div>
                <div style="font-size:11px;color:#64748B">Alerts</div>
              </div>
              <div style="background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:20px;
                   font-size:12px;font-weight:600">● LIVE</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if not st.session_state.session_active:
        # Idle state
        st.markdown("""
        <div style="background:white;border-radius:20px;padding:60px 40px;text-align:center;
             border:2px dashed #E2E8F0;margin:20px 0">
          <div style="font-size:56px;margin-bottom:16px">🎥</div>
          <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;
               color:#0F172A;margin-bottom:8px">No Active Session</div>
          <div style="font-size:14px;color:#64748B;max-width:380px;margin:0 auto;line-height:1.6">
            Click <strong>Start Session</strong> above to begin live monitoring.
            Your webcam will be accessed and all three detection modules will activate.
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Live detection loop ──────────────────────────────────────────────────
    # Try to import detection modules (graceful if model files missing)
    try:
        from eye_movement import process_eye_movement
        EYE_AVAILABLE = True
    except Exception:
        EYE_AVAILABLE = False

    try:
        from head_pose import process_head_pose
        HEAD_AVAILABLE = True
    except Exception:
        HEAD_AVAILABLE = False

    try:
        from mobile_detection import process_mobile_detection
        MOB_AVAILABLE = True
    except Exception:
        MOB_AVAILABLE = False

    # ── Layout: video | right panel ─────────────────────────────────────────
    vid_col, panel_col = st.columns([3, 2])

    with vid_col:
        frame_placeholder = st.empty()
        calib_placeholder = st.empty()

    with panel_col:
        eye_card    = st.empty()
        head_card   = st.empty()
        mobile_card = st.empty()
        risk_col1, risk_col2 = st.columns(2)
        with risk_col1:
            risk_gauge  = st.empty()
        with risk_col2:
            risk_info   = st.empty()
        st.markdown('<div style="font-family:\'Outfit\',sans-serif;font-weight:700;font-size:15px;color:#0F172A;margin:12px 0 8px">Event Timeline</div>', unsafe_allow_html=True)
        timeline_ph = st.empty()

    # ── Open webcam ──────────────────────────────────────────────────────────
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("⚠️ Cannot access webcam. Please allow camera permission and reload.")
        st.session_state.session_active = False
        return

    calib_start = time.time()
    frame_count = 0

    while st.session_state.session_active:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Webcam feed interrupted.")
            break

        frame_count += 1
        now = datetime.datetime.now()
        elapsed = time.time() - calib_start
        calibrating = elapsed <= 5

        # ── Run detection modules ────────────────────────────────────────────
        gaze = "Looking Center"
        head = "Looking at Screen"
        mob  = False

        if EYE_AVAILABLE:
            try:
                frame, gaze = process_eye_movement(frame)
            except Exception:
                pass

        if HEAD_AVAILABLE:
            try:
                if calibrating:
                    _, angles = process_head_pose(frame, None)
                    if angles and not isinstance(angles, str):
                        st.session_state.calibrated_angles = angles
                else:
                    if not st.session_state.calibration_done:
                        st.session_state.calibration_done = True
                        add_event("Head pose calibrated — monitoring active", "info")
                    frame, head = process_head_pose(frame, st.session_state.calibrated_angles)
            except Exception:
                pass

        if MOB_AVAILABLE:
            try:
                frame, mob = process_mobile_detection(frame)
            except Exception:
                pass

        # ── Update session state ─────────────────────────────────────────────
        st.session_state.gaze_direction  = gaze
        st.session_state.head_direction  = head
        st.session_state.mobile_detected = mob

        st.session_state.gaze_counts[gaze] = st.session_state.gaze_counts.get(gaze, 0) + 1
        st.session_state.head_counts[head] = st.session_state.head_counts.get(head, 0) + 1
        if mob:
            st.session_state.mobile_count += 1

        risk = compute_risk_score(gaze, head, mob)
        st.session_state.risk_score = risk
        if frame_count % 5 == 0:
            st.session_state.risk_history.append(risk)
            st.session_state.risk_timestamps.append(now.strftime("%H:%M:%S"))

        # ── Alert timers (mirror main.py logic) ─────────────────────────────
        if head != "Looking at Screen":
            if st.session_state.head_alarm_start is None:
                st.session_state.head_alarm_start = time.time()
            elif time.time() - st.session_state.head_alarm_start >= 3:
                st.session_state.alert_count += 1
                add_event(f"Head turned — {head}", "warning")
                fname = os.path.join(EVIDENCE_DIR, f"head_{int(time.time())}.png")
                cv2.imwrite(fname, frame)
                _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                add_evidence(buf.tobytes(), f"Head: {head}", 0.9)
                st.session_state.head_alarm_start = None
        else:
            st.session_state.head_alarm_start = None

        if gaze != "Looking Center":
            if st.session_state.eye_alarm_start is None:
                st.session_state.eye_alarm_start = time.time()
            elif time.time() - st.session_state.eye_alarm_start >= 3:
                st.session_state.alert_count += 1
                add_event(f"Gaze deviation — {gaze}", "warning")
                fname = os.path.join(EVIDENCE_DIR, f"eye_{int(time.time())}.png")
                cv2.imwrite(fname, frame)
                _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                add_evidence(buf.tobytes(), f"Eye: {gaze}", 0.85)
                st.session_state.eye_alarm_start = None
        else:
            st.session_state.eye_alarm_start = None

        if mob:
            if st.session_state.mobile_alarm_start is None:
                st.session_state.mobile_alarm_start = time.time()
            elif time.time() - st.session_state.mobile_alarm_start >= 2:
                st.session_state.alert_count += 1
                add_event("Mobile phone detected in frame!", "danger")
                fname = os.path.join(EVIDENCE_DIR, f"mobile_{int(time.time())}.png")
                cv2.imwrite(fname, frame)
                _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                add_evidence(buf.tobytes(), "Mobile Phone", 0.92)
                st.session_state.mobile_alarm_start = None
        else:
            st.session_state.mobile_alarm_start = None

        # ── Draw overlays on frame ────────────────────────────────────────────
        overlay = frame.copy()
        h_f, w_f = frame.shape[:2]

        # Calibration banner
        if calibrating:
            cv2.rectangle(overlay, (0, 0), (w_f, 50), (15, 23, 42), -1)
            pct = int(elapsed / 5 * 100)
            cv2.rectangle(overlay, (0, 46), (int(w_f * elapsed / 5), 50), (79, 70, 229), -1)
            cv2.putText(overlay, f"Calibrating... {pct}%  Keep head straight",
                        (12, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (224, 231, 255), 2)

        # Status bar bottom
        bar_y = h_f - 44
        cv2.rectangle(overlay, (0, bar_y), (w_f, h_f), (15, 23, 42), -1)

        gaze_color = (34, 197, 94) if gaze == "Looking Center" else (245, 158, 11)
        head_color = (34, 197, 94) if head == "Looking at Screen" else (245, 158, 11)
        mob_color  = (34, 197, 94) if not mob else (239, 68, 68)

        cv2.putText(overlay, f"EYE: {gaze}", (10, h_f - 16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, gaze_color, 1)
        cv2.putText(overlay, f"HEAD: {head}", (w_f // 3, h_f - 16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, head_color, 1)
        cv2.putText(overlay, f"PHONE: {'YES' if mob else 'NO'}", (2 * w_f // 3, h_f - 16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, mob_color, 1)

        # Risk badge top-right
        rl, rc, _ = risk_level(risk)
        badge_color = (34, 197, 94) if risk < 30 else ((245, 158, 11) if risk < 70 else (239, 68, 68))
        cv2.rectangle(overlay, (w_f - 120, 10), (w_f - 10, 40), (15, 23, 42), -1)
        cv2.rectangle(overlay, (w_f - 120, 10), (w_f - 10, 40), badge_color, 1)
        cv2.putText(overlay, f"RISK: {risk}%", (w_f - 112, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, badge_color, 1)

        # Convert BGR -> RGB for display
        frame_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

        if calibrating:
            calib_placeholder.markdown(f"""
            <div style="background:linear-gradient(135deg,#EFF6FF,#F0F4FF);border-radius:10px;
                 padding:10px 16px;border:1px solid #BFDBFE;font-size:13px;color:#1D4ED8;
                 margin-top:6px;display:flex;align-items:center;gap:8px">
              ⚙️ <strong>Calibrating</strong> — Keep your head straight and look at the screen.
              This takes 5 seconds.
            </div>
            """, unsafe_allow_html=True)
        else:
            calib_placeholder.empty()

        # ── Update right panel ────────────────────────────────────────────────
        # Eye card
        eye_status_text = gaze
        eye_icon = "👁️" if gaze == "Looking Center" else "⚠️"
        eye_color = SUCCESS if gaze == "Looking Center" else WARNING
        eye_card.markdown(detection_card_html(
            "Eye Gaze", eye_status_text, eye_icon, eye_color,
            f'<div style="font-size:11px;color:#64748B;margin-top:6px">dlib 68-point landmarks</div>'
        ), unsafe_allow_html=True)

        # Head card
        head_ok = head == "Looking at Screen"
        head_icon = "🧠" if head_ok else "⚠️"
        head_color = SUCCESS if head_ok else WARNING
        head_card.markdown(detection_card_html(
            "Head Pose", head, head_icon, head_color,
            f'<div style="font-size:11px;color:#64748B;margin-top:6px">PnP pose estimation</div>'
        ), unsafe_allow_html=True)

        # Mobile card
        mob_icon  = "📱" if mob else "✅"
        mob_color = DANGER if mob else SUCCESS
        mob_text  = "PHONE DETECTED!" if mob else "No Device"
        mobile_card.markdown(detection_card_html(
            "Mobile Detection", mob_text, mob_icon, mob_color,
            f'<div style="font-size:11px;color:#64748B;margin-top:6px">YOLOv12 object detection</div>'
        ), unsafe_allow_html=True)

        # Risk gauge
        rl_label, rl_color, _ = risk_level(risk)
        gauge_colors = [SUCCESS, WARNING, DANGER]
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1,
                          "tickcolor": "#94A3B8", "tickfont": {"size": 9}},
                "bar": {"color": rl_color, "thickness": 0.25},
                "bgcolor": "white",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30],  "color": "#F0FDF4"},
                    {"range": [30, 70], "color": "#FFFBEB"},
                    {"range": [70, 100],"color": "#FFF5F5"},
                ],
                "threshold": {"line": {"color": DANGER, "width": 2},
                               "thickness": 0.75, "value": 80},
            },
            number={"font": {"size": 24, "family": "Outfit", "color": rl_color},
                    "suffix": "%"},
        ))
        fig_gauge.update_layout(
            height=160,
            margin=dict(l=8, r=8, t=24, b=4),
            paper_bgcolor="white",
            font=dict(family="Inter"),
        )
        risk_gauge.plotly_chart(fig_gauge, use_container_width=True,
                                 config={"displayModeBar": False})

        risk_info.markdown(f"""
        <div style="background:white;border-radius:14px;padding:14px;
             border:1px solid #F1F5F9;text-align:center">
          <div style="font-size:11px;color:#64748B;margin-bottom:6px">Risk Level</div>
          <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:800;
               color:{rl_color}">{rl_label}</div>
          <div style="font-size:11px;color:#94A3B8;margin-top:4px">
            Alerts: {st.session_state.alert_count}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Timeline (last 6 events)
        events = st.session_state.events[-6:]
        timeline_html = ""
        for ev in reversed(events):
            timeline_html += timeline_item_html(ev["time"], ev["message"], ev["level"])
        if not timeline_html:
            timeline_html = '<div style="font-size:13px;color:#94A3B8;padding:12px 0">No events yet</div>'
        timeline_ph.markdown(
            f'<div style="background:white;border-radius:14px;padding:14px;'
            f'border:1px solid #F1F5F9">{timeline_html}</div>',
            unsafe_allow_html=True
        )

        time.sleep(0.04)  # ~25fps refresh

    cap.release()
