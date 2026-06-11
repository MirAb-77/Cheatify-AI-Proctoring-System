import streamlit as st
import json
import csv
import io
import datetime
import pandas as pd
from utils.helpers import (
    PRIMARY, SECONDARY, ACCENT, SUCCESS, WARNING, DANGER,
    risk_level, format_duration, get_analytics_df
)


def _section(title):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin:24px 0 12px">
      <div style="height:3px;width:28px;background:linear-gradient(90deg,{PRIMARY},{SECONDARY});
           border-radius:2px"></div>
      <div style="font-family:'Outfit',sans-serif;font-size:15px;font-weight:700;
           color:#0F172A">{title}</div>
      <div style="flex:1;height:1px;background:#F1F5F9"></div>
    </div>
    """, unsafe_allow_html=True)


def build_report_dict():
    risk  = st.session_state.risk_score
    rl, _, _ = risk_level(risk)
    gaze_counts = st.session_state.gaze_counts
    head_counts = st.session_state.head_counts
    dur = format_duration(st.session_state.session_start)

    gaze_devs  = sum(v for k, v in gaze_counts.items() if k != "Looking Center")
    head_events = sum(v for k, v in head_counts.items() if k != "Looking at Screen")

    report = {
        "report_generated": datetime.datetime.now().isoformat(),
        "session_id":       st.session_state.session_id or "N/A",
        "duration":         dur,
        "risk_score":       risk,
        "risk_level":       rl,
        "alert_count":      st.session_state.alert_count,
        "evidence_frames":  len(st.session_state.evidence),
        "eye_gaze_summary": gaze_counts,
        "head_pose_summary": head_counts,
        "mobile_detections": st.session_state.mobile_count,
        "gaze_deviations":  gaze_devs,
        "head_movements":   head_events,
        "events": st.session_state.events,
        "recommendation": (
            "No suspicious activity detected. Student behaviour appears normal."
            if risk < 30 else
            "Moderate suspicious activity detected. Manual review recommended."
            if risk < 70 else
            "High risk of cheating behaviour. Immediate intervention required."
        ),
    }
    return report


def render_reports():
    st.markdown('<div class="page-title">Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-breadcrumb">Generate and export comprehensive session reports</div>',
                unsafe_allow_html=True)

    report = build_report_dict()
    risk   = report["risk_score"]
    rl     = report["risk_level"]
    rc     = SUCCESS if risk < 30 else (WARNING if risk < 70 else DANGER)

    # ── Report header card ───────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#4F46E5,#7C3AED);border-radius:20px;
         padding:32px;color:white;margin-bottom:20px">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px">
        <div>
          <div style="font-size:12px;opacity:0.7;letter-spacing:0.1em;text-transform:uppercase;
               margin-bottom:8px;font-family:'Inter',sans-serif">Examination Report</div>
          <div style="font-family:'Outfit',sans-serif;font-size:28px;font-weight:800;
               margin-bottom:4px">Cheatify Proctoring Report</div>
          <div style="opacity:0.75;font-size:14px">Generated: {report['report_generated'][:19].replace('T', ' ')}</div>
        </div>
        <div style="background:rgba(255,255,255,0.15);border-radius:14px;padding:20px 28px;text-align:center">
          <div style="font-size:11px;opacity:0.7;margin-bottom:4px">RISK SCORE</div>
          <div style="font-family:'Outfit',sans-serif;font-size:40px;font-weight:800;
               line-height:1">{risk}</div>
          <div style="font-size:13px;opacity:0.8">{rl}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Candidate summary ────────────────────────────────────────────────────
    _section("Candidate Summary")
    c1, c2, c3, c4 = st.columns(4)
    for col, icon, label, val, color in [
        (c1, "🆔", "Session ID",       report["session_id"],     PRIMARY),
        (c2, "⏱️", "Duration",         report["duration"],        ACCENT),
        (c3, "🚨", "Total Alerts",     str(report["alert_count"]),DANGER),
        (c4, "🖼️", "Evidence Frames",  str(report["evidence_frames"]),SECONDARY),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:18px 16px;
                 border:1px solid #F1F5F9;box-shadow:0 1px 4px rgba(0,0,0,0.04)">
              <div style="font-size:22px;margin-bottom:8px">{icon}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:800;
                   color:{color};margin-bottom:4px">{val}</div>
              <div style="font-size:12px;color:#64748B">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Detection summaries ──────────────────────────────────────────────────
    _section("Detection Module Summary")
    gc = report["eye_gaze_summary"]
    hc = report["head_pose_summary"]

    det_col1, det_col2, det_col3 = st.columns(3)
    with det_col1:
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:18px;
             border:1px solid #F1F5F9;border-top:3px solid {PRIMARY}">
          <div style="font-family:'Outfit',sans-serif;font-weight:700;margin-bottom:12px">👁️ Eye Gaze</div>
        """, unsafe_allow_html=True)
        for k, v in gc.items():
            pct = round(v / max(sum(gc.values()), 1) * 100, 1)
            bar_color = SUCCESS if k == "Looking Center" else WARNING
            st.markdown(f"""
            <div style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px">
                <span style="color:#374151">{k}</span>
                <span style="color:#64748B;font-weight:600">{v} ({pct}%)</span>
              </div>
              <div style="height:5px;background:#F1F5F9;border-radius:3px">
                <div style="height:5px;width:{pct}%;background:{bar_color};border-radius:3px"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with det_col2:
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:18px;
             border:1px solid #F1F5F9;border-top:3px solid {SECONDARY}">
          <div style="font-family:'Outfit',sans-serif;font-weight:700;margin-bottom:12px">🧠 Head Pose</div>
        """, unsafe_allow_html=True)
        for k, v in hc.items():
            pct = round(v / max(sum(hc.values()), 1) * 100, 1)
            bar_color = SUCCESS if k == "Looking at Screen" else WARNING
            st.markdown(f"""
            <div style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px">
                <span style="color:#374151">{k}</span>
                <span style="color:#64748B;font-weight:600">{v} ({pct}%)</span>
              </div>
              <div style="height:5px;background:#F1F5F9;border-radius:3px">
                <div style="height:5px;width:{pct}%;background:{bar_color};border-radius:3px"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with det_col3:
        mob_count = report["mobile_detections"]
        mob_color = DANGER if mob_count > 0 else SUCCESS
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:18px;
             border:1px solid #F1F5F9;border-top:3px solid {ACCENT}">
          <div style="font-family:'Outfit',sans-serif;font-weight:700;margin-bottom:12px">📱 Mobile Detection</div>
          <div style="text-align:center;padding:20px 0">
            <div style="font-size:48px;margin-bottom:8px">{'⚠️' if mob_count > 0 else '✅'}</div>
            <div style="font-family:'Outfit',sans-serif;font-size:28px;font-weight:800;
                 color:{mob_color}">{mob_count}</div>
            <div style="font-size:12px;color:#64748B;margin-top:4px">Detection Events</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── AI Behaviour Report ─────────────────────────────────────────────────
    _section("AI Behaviour Analysis")
    gaze_devs  = report["gaze_deviations"]
    head_events = report["head_movements"]
    mob_events  = report["mobile_detections"]

    if risk == 0:
        behaviour = "✅ **Normal Behaviour** — No suspicious activity was detected during this session."
        detail = "The candidate maintained consistent eye contact with the screen and kept a stable head position throughout."
        behaviour_color = "#F0FDF4"; border_color = SUCCESS
    elif risk < 30:
        behaviour = "🟢 **Low Risk** — Minor deviations were observed but fall within acceptable thresholds."
        detail = f"Eye gaze deviated {gaze_devs} times and head moved {head_events} times, both within normal ranges."
        behaviour_color = "#F0FDF4"; border_color = SUCCESS
    elif risk < 70:
        behaviour = "🟡 **Moderate Risk** — Suspicious behaviour patterns detected. Manual review recommended."
        detail = f"Repeated gaze deviations ({gaze_devs} events) and head movements ({head_events} events) suggest possible copying from an external source."
        behaviour_color = "#FFFBEB"; border_color = WARNING
    else:
        behaviour = "🔴 **High Risk** — Strong indicators of cheating behaviour. Immediate intervention recommended."
        detail = f"Mobile phone detected {mob_events} time(s). Significant gaze ({gaze_devs}) and head ({head_events}) deviations confirm suspicious behaviour."
        behaviour_color = "#FFF5F5"; border_color = DANGER

    st.markdown(f"""
    <div style="background:{behaviour_color};border-radius:14px;padding:20px 24px;
         border:1px solid {border_color}44;border-left:4px solid {border_color}">
      <div style="font-size:15px;font-weight:600;color:#0F172A;margin-bottom:8px">{behaviour}</div>
      <div style="font-size:13px;color:#374151;line-height:1.6">{detail}</div>
      <div style="margin-top:12px;font-size:13px;color:#64748B">
        <strong>Recommendation:</strong> {report['recommendation']}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Event Timeline ────────────────────────────────────────────────────────
    _section("Event Timeline")
    events = st.session_state.events
    if events:
        ev_data = pd.DataFrame(events)
        st.dataframe(ev_data, use_container_width=True, hide_index=True,
                     column_config={
                         "time":    st.column_config.TextColumn("Time"),
                         "message": st.column_config.TextColumn("Event"),
                         "level":   st.column_config.TextColumn("Level"),
                     })
    else:
        st.info("No events recorded in this session.")

    # ── Export ────────────────────────────────────────────────────────────────
    _section("Export Report")
    ex1, ex2, ex3 = st.columns(3)

    with ex1:
        json_str = json.dumps(report, indent=2, default=str)
        st.download_button(
            "📄 Export JSON",
            data=json_str,
            file_name=f"cheatify_report_{report['session_id']}.json",
            mime="application/json",
            use_container_width=True,
        )

    with ex2:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["Field", "Value"])
        flat = {
            "Session ID":        report["session_id"],
            "Duration":          report["duration"],
            "Risk Score":        report["risk_score"],
            "Risk Level":        report["risk_level"],
            "Alert Count":       report["alert_count"],
            "Evidence Frames":   report["evidence_frames"],
            "Gaze Deviations":   report["gaze_deviations"],
            "Head Movements":    report["head_movements"],
            "Mobile Detections": report["mobile_detections"],
            "Recommendation":    report["recommendation"],
        }
        for k, v in flat.items():
            writer.writerow([k, v])
        st.download_button(
            "📊 Export CSV",
            data=buf.getvalue(),
            file_name=f"cheatify_report_{report['session_id']}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with ex3:
        # Simple text report
        lines = [
            "CHEATIFY PROCTORING REPORT",
            "=" * 40,
            f"Session ID  : {report['session_id']}",
            f"Generated   : {report['report_generated'][:19]}",
            f"Duration    : {report['duration']}",
            f"Risk Score  : {report['risk_score']}% ({report['risk_level']})",
            f"Total Alerts: {report['alert_count']}",
            "",
            "DETECTION SUMMARY",
            "-" * 40,
            f"Gaze Deviations  : {report['gaze_deviations']}",
            f"Head Movements   : {report['head_movements']}",
            f"Mobile Detections: {report['mobile_detections']}",
            "",
            "RECOMMENDATION",
            "-" * 40,
            report["recommendation"],
            "",
            "EVENT LOG",
            "-" * 40,
        ]
        for ev in events:
            lines.append(f"[{ev['time']}] [{ev['level'].upper()}] {ev['message']}")
        txt = "\n".join(lines)
        st.download_button(
            "📝 Export TXT",
            data=txt,
            file_name=f"cheatify_report_{report['session_id']}.txt",
            mime="text/plain",
            use_container_width=True,
        )
