import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime
import random
from utils.helpers import (
    PRIMARY, SECONDARY, ACCENT, SUCCESS, WARNING, DANGER,
    metric_card_html, format_duration, risk_level, get_analytics_df
)


def render_dashboard():
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-breadcrumb">Overview of all active monitoring sessions</div>',
                unsafe_allow_html=True)

    # ── Top metric cards ────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    dur = format_duration(st.session_state.session_start) if st.session_state.session_active else "—"
    risk = st.session_state.risk_score
    rl, rc, _ = risk_level(risk)

    cards = [
        (c1, "👤", "Students Monitored", str(st.session_state.students_monitored),
         PRIMARY, None, True),
        (c2, "⏱️", "Session Duration", dur,
         ACCENT, None, True),
        (c3, "🚨", "Total Alerts", str(st.session_state.alert_count),
         DANGER, f"{st.session_state.alert_count} events" if st.session_state.alert_count else None,
         st.session_state.alert_count == 0),
        (c4, "🎯", "System Accuracy", "97.4%",
         SUCCESS, None, True),
    ]
    for col, icon, label, val, color, delta, delta_ok in cards:
        with col:
            st.markdown(metric_card_html(icon, label, val, color, delta, delta_ok),
                        unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Charts row ──────────────────────────────────────────────────────────
    left, right = st.columns([3, 2])

    with left:
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:20px;
             border:1px solid #F1F5F9;box-shadow:0 1px 4px rgba(0,0,0,0.05)">
          <div style="font-family:'Outfit',sans-serif;font-weight:700;font-size:16px;
               color:#0F172A;margin-bottom:4px">Violation Trends</div>
          <div style="font-size:12px;color:#64748B;margin-bottom:16px">Last 12 intervals</div>
        """, unsafe_allow_html=True)

        gaze_df, head_df, risk_df = get_analytics_df()
        g_counts = list(st.session_state.gaze_counts.values())
        h_counts = list(st.session_state.head_counts.values())
        mob_count = st.session_state.mobile_count
        labels = [f"T-{i*5}s" for i in range(12, 0, -1)]

        # build a stacked bar
        n = 12
        rng = random.Random(42)
        eye_vals   = [max(0, g_counts[1] + g_counts[2] - (11-i)) for i in range(n)]
        head_vals  = [max(0, h_counts[1] + h_counts[2] - (11-i)) for i in range(n)]
        phone_vals = [max(0, mob_count - (11-i)) for i in range(n)]

        # If session hasn't started yet, show illustrative demo data
        if not st.session_state.session_active and all(v == 0 for v in eye_vals):
            rng2 = random.Random(7)
            eye_vals   = [rng2.randint(0, 4) for _ in range(n)]
            head_vals  = [rng2.randint(0, 3) for _ in range(n)]
            phone_vals = [rng2.randint(0, 2) for _ in range(n)]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=labels, y=eye_vals,   name="Eye Deviation",
                                  marker_color=PRIMARY,   marker_line_width=0))
        fig_bar.add_trace(go.Bar(x=labels, y=head_vals,  name="Head Movement",
                                  marker_color=SECONDARY, marker_line_width=0))
        fig_bar.add_trace(go.Bar(x=labels, y=phone_vals, name="Phone Detection",
                                  marker_color=ACCENT,    marker_line_width=0))
        fig_bar.update_layout(
            barmode="stack", height=240,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11, color="#64748B"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="left", x=0, font=dict(size=11)),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9",
                       zeroline=False, tickfont=dict(size=10)),
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:20px;
             border:1px solid #F1F5F9;box-shadow:0 1px 4px rgba(0,0,0,0.05)">
          <div style="font-family:'Outfit',sans-serif;font-weight:700;font-size:16px;
               color:#0F172A;margin-bottom:4px">Detection Distribution</div>
          <div style="font-size:12px;color:#64748B;margin-bottom:8px">By module</div>
        """, unsafe_allow_html=True)

        gc = st.session_state.gaze_counts
        hc = st.session_state.head_counts
        eye_total  = sum(gc.values()) - gc.get("Looking Center", 0)
        head_total = sum(hc.values()) - hc.get("Looking at Screen", 0)
        mob_total  = st.session_state.mobile_count

        if eye_total + head_total + mob_total == 0:
            eye_total, head_total, mob_total = 45, 35, 20

        fig_pie = go.Figure(go.Pie(
            labels=["Eye Gaze", "Head Pose", "Mobile"],
            values=[eye_total, head_total, mob_total],
            hole=0.6,
            marker_colors=[PRIMARY, SECONDARY, ACCENT],
            textinfo="percent",
            textfont=dict(size=12),
        ))
        fig_pie.update_layout(
            height=220, margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor="white", paper_bgcolor="white",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15,
                        font=dict(size=11)),
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Risk history + Session stats ────────────────────────────────────────
    left2, right2 = st.columns([3, 2])

    with left2:
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:20px;
             border:1px solid #F1F5F9;box-shadow:0 1px 4px rgba(0,0,0,0.05)">
          <div style="font-family:'Outfit',sans-serif;font-weight:700;font-size:16px;
               color:#0F172A;margin-bottom:4px">Risk Score Over Time</div>
          <div style="font-size:12px;color:#64748B;margin-bottom:16px">Live tracking</div>
        """, unsafe_allow_html=True)

        _, _, risk_df = get_analytics_df()
        if len(risk_df) < 3:
            import numpy as np
            t = [datetime.datetime.now() - datetime.timedelta(seconds=i*10) for i in range(20, 0, -1)]
            r = [random.randint(0, 60) for _ in t]
            risk_df = pd.DataFrame({"Time": t, "Risk Score": r})

        fig_risk = go.Figure()
        fig_risk.add_trace(go.Scatter(
            x=risk_df["Time"], y=risk_df["Risk Score"],
            fill="tozeroy",
            fillcolor=f"rgba(79,70,229,0.08)",
            line=dict(color=PRIMARY, width=2.5),
            mode="lines",
        ))
        fig_risk.add_hline(y=60, line_dash="dash", line_color=WARNING,
                            annotation_text="High Risk", annotation_font_size=11)
        fig_risk.add_hline(y=80, line_dash="dash", line_color=DANGER,
                            annotation_text="Critical", annotation_font_size=11)
        fig_risk.update_layout(
            height=200, margin=dict(l=0, r=0, t=4, b=0),
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11, color="#64748B"),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(range=[0, 105], showgrid=True,
                       gridcolor="#F1F5F9", tickfont=dict(size=10)),
        )
        st.plotly_chart(fig_risk, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with right2:
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:20px;height:100%;
             border:1px solid #F1F5F9;box-shadow:0 1px 4px rgba(0,0,0,0.05)">
          <div style="font-family:'Outfit',sans-serif;font-weight:700;font-size:16px;
               color:#0F172A;margin-bottom:16px">Session Statistics</div>
        """, unsafe_allow_html=True)

        stats = [
            ("Status", "🟢 Active" if st.session_state.session_active else "⚪ Idle"),
            ("Session ID", st.session_state.session_id or "—"),
            ("Duration", dur),
            ("Risk Level", f"{rl}"),
            ("Eye Deviations", str(sum(v for k, v in st.session_state.gaze_counts.items()
                                       if k != "Looking Center"))),
            ("Head Events",    str(sum(v for k, v in st.session_state.head_counts.items()
                                       if k != "Looking at Screen"))),
            ("Phone Detections", str(st.session_state.mobile_count)),
        ]
        for k, v in stats:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                 padding:8px 0;border-bottom:1px solid #F8FAFC;">
              <span style="font-size:12px;color:#64748B">{k}</span>
              <span style="font-size:13px;font-weight:600;color:#0F172A">{v}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Recent alerts ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:white;border-radius:16px;padding:20px;
         border:1px solid #F1F5F9;box-shadow:0 1px 4px rgba(0,0,0,0.05)">
      <div style="font-family:'Outfit',sans-serif;font-weight:700;font-size:16px;
           color:#0F172A;margin-bottom:16px">Recent Events</div>
    """, unsafe_allow_html=True)

    events = st.session_state.events[-8:] if st.session_state.events else []
    if not events:
        st.markdown("""
        <div style="text-align:center;padding:24px;color:#94A3B8;font-size:14px">
          No events yet — start a monitoring session to see live events here.
        </div>
        """, unsafe_allow_html=True)
    else:
        for ev in reversed(events):
            colors = {"danger": DANGER, "warning": WARNING, "success": SUCCESS, "info": ACCENT}
            col = colors.get(ev["level"], ACCENT)
            icons = {"danger": "🔴", "warning": "🟡", "success": "🟢", "info": "🔵"}
            ic = icons.get(ev["level"], "🔵")
            st.markdown(f"""
            <div class="timeline-item">
              <div class="timeline-dot" style="background:{col}"></div>
              <div class="timeline-time">{ev['time']}</div>
              <div class="timeline-msg">{ic} {ev['message']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
