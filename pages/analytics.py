import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime
import random
from utils.helpers import (
    PRIMARY, SECONDARY, ACCENT, SUCCESS, WARNING, DANGER,
    get_analytics_df
)

CHART_LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Inter", size=12, color="#374151"),
    margin=dict(l=16, r=16, t=8, b=8),
    showlegend=True,
)


def _card(title, sub=""):
    return f"""
    <div style="background:white;border-radius:16px;padding:20px;
         border:1px solid #F1F5F9;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:4px">
      <div style="font-family:'Outfit',sans-serif;font-weight:700;font-size:16px;
           color:#0F172A;margin-bottom:2px">{title}</div>
      <div style="font-size:12px;color:#64748B;margin-bottom:12px">{sub}</div>
    """


def render_analytics():
    st.markdown('<div class="page-title">Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-breadcrumb">Deep-dive into detection statistics and patterns</div>',
                unsafe_allow_html=True)

    gaze_df, head_df, risk_df = get_analytics_df()

    # ── Use demo data if session hasn't run ──────────────────────────────────
    if gaze_df["Count"].sum() == 0:
        rng = random.Random(99)
        gaze_df = pd.DataFrame([
            {"Category": "Looking Center", "Count": 280, "Percentage": 70.0},
            {"Category": "Looking Left",   "Count": 50,  "Percentage": 12.5},
            {"Category": "Looking Right",  "Count": 40,  "Percentage": 10.0},
            {"Category": "Looking Up",     "Count": 20,  "Percentage": 5.0},
            {"Category": "Looking Down",   "Count": 10,  "Percentage": 2.5},
        ])
        head_df = pd.DataFrame([
            {"Category": "Looking at Screen", "Count": 260, "Percentage": 65.0},
            {"Category": "Looking Left",      "Count": 60,  "Percentage": 15.0},
            {"Category": "Looking Right",     "Count": 48,  "Percentage": 12.0},
            {"Category": "Looking Up",        "Count": 20,  "Percentage": 5.0},
            {"Category": "Looking Down",      "Count": 8,   "Percentage": 2.0},
            {"Category": "Tilted",            "Count": 4,   "Percentage": 1.0},
        ])
        t = [datetime.datetime.now() - datetime.timedelta(seconds=i*10) for i in range(30, 0, -1)]
        r_vals = [rng.randint(0, 70) for _ in t]
        risk_df = pd.DataFrame({"Time": t, "Risk Score": r_vals})

    col_l, col_r = st.columns(2)

    # ── Eye Movement Frequency ───────────────────────────────────────────────
    with col_l:
        st.markdown(_card("Eye Movement Frequency", "Distribution across gaze directions"),
                    unsafe_allow_html=True)
        colors_eye = [PRIMARY if c == "Looking Center" else SECONDARY
                      for c in gaze_df["Category"]]
        fig_eye = go.Figure(go.Bar(
            x=gaze_df["Category"], y=gaze_df["Count"],
            marker_color=colors_eye,
            marker_line_width=0,
            text=gaze_df["Percentage"].apply(lambda x: f"{x}%"),
            textposition="outside",
            textfont=dict(size=11),
        ))
        fig_eye.update_layout(height=280, **CHART_LAYOUT,
                               xaxis=dict(showgrid=False, tickangle=-15),
                               yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
                               showlegend=False)
        st.plotly_chart(fig_eye, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Head Pose Frequency ──────────────────────────────────────────────────
    with col_r:
        st.markdown(_card("Head Pose Frequency", "Distribution across head orientations"),
                    unsafe_allow_html=True)
        colors_head = [SUCCESS if c == "Looking at Screen" else WARNING
                       for c in head_df["Category"]]
        fig_head = go.Figure(go.Bar(
            x=head_df["Category"], y=head_df["Count"],
            marker_color=colors_head,
            marker_line_width=0,
            text=head_df["Percentage"].apply(lambda x: f"{x}%"),
            textposition="outside",
            textfont=dict(size=11),
        ))
        fig_head.update_layout(height=280, **CHART_LAYOUT,
                                xaxis=dict(showgrid=False, tickangle=-15),
                                yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
                                showlegend=False)
        st.plotly_chart(fig_head, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Risk Score Timeline ──────────────────────────────────────────────────
    st.markdown(_card("Risk Score Timeline", "Cheating risk percentage over session duration"),
                unsafe_allow_html=True)
    fig_risk = go.Figure()
    fig_risk.add_trace(go.Scatter(
        x=risk_df["Time"], y=risk_df["Risk Score"],
        fill="tozeroy", fillcolor="rgba(79,70,229,0.07)",
        line=dict(color=PRIMARY, width=2.5),
        mode="lines+markers",
        marker=dict(size=4, color=PRIMARY),
        name="Risk Score",
    ))
    # Threshold bands
    fig_risk.add_hrect(y0=0,  y1=30, fillcolor=SUCCESS, opacity=0.03, line_width=0)
    fig_risk.add_hrect(y0=30, y1=70, fillcolor=WARNING, opacity=0.04, line_width=0)
    fig_risk.add_hrect(y0=70, y1=100,fillcolor=DANGER,  opacity=0.04, line_width=0)
    fig_risk.add_hline(y=30, line_dash="dot", line_color=SUCCESS,
                        annotation_text="Low threshold",  annotation_font_size=10)
    fig_risk.add_hline(y=70, line_dash="dot", line_color=WARNING,
                        annotation_text="High threshold", annotation_font_size=10)
    fig_risk.update_layout(
        height=260, **CHART_LAYOUT,
        xaxis=dict(showgrid=False),
        yaxis=dict(range=[0, 105], showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        showlegend=False,
    )
    st.plotly_chart(fig_risk, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Detection Distribution + Alert Breakdown ────────────────────────────
    col3, col4 = st.columns([1, 1])

    with col3:
        st.markdown(_card("Risk Distribution", "How often each risk band was active"),
                    unsafe_allow_html=True)
        if len(risk_df) > 0:
            bins = [0, 30, 70, 100]
            labels_r = ["Low (0-30)", "Medium (30-70)", "High (70-100)"]
            counts_r = [
                int((risk_df["Risk Score"] < 30).sum()),
                int(((risk_df["Risk Score"] >= 30) & (risk_df["Risk Score"] < 70)).sum()),
                int((risk_df["Risk Score"] >= 70).sum()),
            ]
        else:
            labels_r = ["Low (0-30)", "Medium (30-70)", "High (70-100)"]
            counts_r = [20, 12, 5]

        fig_dist = go.Figure(go.Pie(
            labels=labels_r, values=counts_r,
            hole=0.55,
            marker_colors=[SUCCESS, WARNING, DANGER],
            textinfo="label+percent",
            textfont=dict(size=11),
        ))
        fig_dist.update_layout(height=260, **CHART_LAYOUT,
                                legend=dict(orientation="h", yanchor="bottom", y=-0.2))
        st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown(_card("Module Alert Breakdown", "Total alerts raised per detection module"),
                    unsafe_allow_html=True)
        gaze_alerts   = sum(v for k, v in st.session_state.gaze_counts.items()
                            if k != "Looking Center")
        head_alerts   = sum(v for k, v in st.session_state.head_counts.items()
                            if k != "Looking at Screen")
        mobile_alerts = st.session_state.mobile_count
        if gaze_alerts + head_alerts + mobile_alerts == 0:
            gaze_alerts, head_alerts, mobile_alerts = 45, 32, 14

        fig_mod = go.Figure(go.Bar(
            x=["Eye Gaze", "Head Pose", "Mobile Detection"],
            y=[gaze_alerts, head_alerts, mobile_alerts],
            marker_color=[PRIMARY, SECONDARY, ACCENT],
            marker_line_width=0,
            text=[gaze_alerts, head_alerts, mobile_alerts],
            textposition="outside",
        ))
        fig_mod.update_layout(
            height=260, **CHART_LAYOUT,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
            showlegend=False,
        )
        st.plotly_chart(fig_mod, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Raw data table ────────────────────────────────────────────────────────
    with st.expander("📊 Raw Detection Data", expanded=False):
        tab1, tab2 = st.tabs(["Eye Movement", "Head Pose"])
        with tab1:
            st.dataframe(gaze_df, use_container_width=True, hide_index=True)
        with tab2:
            st.dataframe(head_df, use_container_width=True, hide_index=True)
