"""
Cheatify — AI-Powered Exam Proctoring System
Main Streamlit application entry point.

Run with:
    streamlit run app.py
"""

import streamlit as st
import sys, os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.styles  import GLOBAL_CSS
from utils.helpers import init_session_state, PRIMARY, SECONDARY

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cheatify — AI Proctoring",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Apply global styles ───────────────────────────────────────────────────────
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Initialise session state ──────────────────────────────────────────────────
init_session_state()

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown(f"""
    <div style="padding:12px 0 24px;text-align:center">
      <div style="display:inline-flex;align-items:center;justify-content:center;
           width:52px;height:52px;border-radius:16px;
           background:rgba(255,255,255,0.15);margin-bottom:10px;font-size:28px">
        🎓
      </div>
      <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:800;
           color:white;letter-spacing:-0.5px">Cheatify</div>
      <div style="font-size:11px;color:rgba(255,255,255,0.45);letter-spacing:0.08em;
           text-transform:uppercase;margin-top:2px">AI Proctoring v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="border-color:rgba(255,255,255,0.1);margin:0 0 12px"/>', unsafe_allow_html=True)

    # Nav
    pages = {
        "🏠  Home":            "landing",
        "📊  Dashboard":       "dashboard",
        "🎥  Live Monitoring": "monitoring",
        "📈  Analytics":       "analytics",
        "🖼️  Evidence":        "evidence",
        "📋  Reports":         "reports",
    }
    current = st.session_state.page
    for label, key in pages.items():
        is_active = current == key
        btn_style = (
            "background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.25);"
            if is_active else
            "background:transparent;border:1px solid transparent;"
        )
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown('<hr style="border-color:rgba(255,255,255,0.1);margin:12px 0"/>', unsafe_allow_html=True)

    # Session status in sidebar
    if st.session_state.session_active:
        st.markdown(f"""
        <div style="background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.3);
             border-radius:10px;padding:10px 12px;margin:0 0 12px">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">
            <div style="width:6px;height:6px;border-radius:50%;background:#22C55E;
                 box-shadow:0 0 0 3px rgba(34,197,94,0.2)"></div>
            <span style="font-size:12px;font-weight:600;color:#86EFAC">Session Active</span>
          </div>
          <div style="font-size:11px;color:rgba(255,255,255,0.5)">
            ID: {st.session_state.session_id or '—'}
          </div>
          <div style="font-size:11px;color:rgba(255,255,255,0.5)">
            Alerts: {st.session_state.alert_count}
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px 12px;
             margin:0 0 12px">
          <div style="font-size:12px;color:rgba(255,255,255,0.3)">● No active session</div>
        </div>
        """, unsafe_allow_html=True)

    # Module status
    st.markdown("""
    <div style="font-size:10px;text-transform:uppercase;letter-spacing:0.1em;
         color:rgba(255,255,255,0.3);margin-bottom:8px">Detection Modules</div>
    """, unsafe_allow_html=True)
    for mod, icon in [("Eye Tracking", "👁️"), ("Head Pose", "🧠"), ("Mobile Detect", "📱")]:
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
             padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.06)">
          <span style="font-size:12px;color:rgba(255,255,255,0.55)">{icon} {mod}</span>
          <span style="font-size:10px;color:#86EFAC;font-weight:600">READY</span>
        </div>
        """, unsafe_allow_html=True)

    # Bottom
    st.markdown("""
    <div style="position:absolute;bottom:16px;left:16px;right:16px;text-align:center;
         font-size:10px;color:rgba(255,255,255,0.2)">
      Built with ❤️ · OpenCV · dlib · YOLOv12
    </div>
    """, unsafe_allow_html=True)

# ── Route to pages ─────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "landing":
    from pages.landing    import render_landing;    render_landing()
elif page == "dashboard":
    from pages.dashboard  import render_dashboard;  render_dashboard()
elif page == "monitoring":
    from pages.monitoring import render_monitoring; render_monitoring()
elif page == "analytics":
    from pages.analytics  import render_analytics;  render_analytics()
elif page == "evidence":
    from pages.evidence   import render_evidence;   render_evidence()
elif page == "reports":
    from pages.reports    import render_reports;    render_reports()
