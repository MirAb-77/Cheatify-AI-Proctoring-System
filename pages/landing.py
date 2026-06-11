import streamlit as st
from utils.helpers import PRIMARY, SECONDARY, ACCENT, SUCCESS


def render_landing():
    # Hero section
    st.markdown("""
    <div class="landing-hero">
      <div style="position:relative;z-index:2">
        <div style="display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,0.12);
             border-radius:30px;padding:6px 18px;margin-bottom:24px;font-size:13px;font-weight:500;
             letter-spacing:0.05em;border:1px solid rgba(255,255,255,0.2);">
          🎓 &nbsp; AI-Powered Exam Proctoring System
        </div>
        <div class="landing-title">
          Cheat<span style="background:linear-gradient(135deg,#A5B4FC,#C4B5FD);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">ify</span>
        </div>
        <div class="landing-sub">
          Real-time exam integrity monitoring powered by computer vision.
          Detect cheating before it happens.
        </div>
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;position:relative">
          <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);
               border-radius:12px;padding:16px 24px;text-align:center;min-width:100px;">
            <div style="font-family:'Outfit',sans-serif;font-size:28px;font-weight:800;">99%</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.65);margin-top:2px;">Accuracy</div>
          </div>
          <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);
               border-radius:12px;padding:16px 24px;text-align:center;min-width:100px;">
            <div style="font-family:'Outfit',sans-serif;font-size:28px;font-weight:800;">3</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.65);margin-top:2px;">AI Modules</div>
          </div>
          <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);
               border-radius:12px;padding:16px 24px;text-align:center;min-width:100px;">
            <div style="font-family:'Outfit',sans-serif;font-size:28px;font-weight:800;">&lt;50ms</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.65);margin-top:2px;">Latency</div>
          </div>
          <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);
               border-radius:12px;padding:16px 24px;text-align:center;min-width:100px;">
            <div style="font-family:'Outfit',sans-serif;font-size:28px;font-weight:800;">Live</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.65);margin-top:2px;">Webcam</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # Feature cards
    st.markdown("""
    <div class="section-header" style="text-align:center">Three Modules. One System.</div>
    <div class="section-sub" style="text-align:center">
        Each detection engine runs in parallel on every video frame.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    feature_cards = [
        (c1, "👁️", "Eye Gaze Tracking", "#4F46E5",
         "Tracks pupil position using 68 facial landmarks to detect when students look away from the screen."),
        (c2, "🧠", "Head Pose Estimation", "#7C3AED",
         "Analyses 3D head orientation using PnP solving to flag sustained head turns beyond safe thresholds."),
        (c3, "📱", "Mobile Detection", "#06B6D4",
         "YOLOv12-based object detector identifies mobile phones in the camera frame with >80% confidence."),
    ]
    for col, icon, title, color, desc in feature_cards:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;padding:28px 20px">
              <div style="font-size:40px;margin-bottom:12px">{icon}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:17px;font-weight:700;
                   color:#0F172A;margin-bottom:10px">{title}</div>
              <div style="font-size:13px;color:#64748B;line-height:1.6">{desc}</div>
              <div style="height:3px;background:linear-gradient(90deg,{color},{color}88);
                   border-radius:2px;margin-top:20px;"></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # How it works
    st.markdown("""
    <div style="background:white;border-radius:20px;padding:32px;border:1px solid #F1F5F9;
         box-shadow:0 1px 4px rgba(0,0,0,0.05);">
      <div class="section-header" style="margin-bottom:20px">How It Works</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;">
    """, unsafe_allow_html=True)

    steps = [
        ("1", "📷", "Camera Input", "Live webcam feed captured at 30fps"),
        ("2", "🔍", "Frame Analysis", "Each frame passes through all 3 AI modules simultaneously"),
        ("3", "⚡", "Risk Scoring", "Violations are weighted and combined into a live risk score"),
        ("4", "🚨", "Alert & Log",  "Suspicious frames saved with timestamp and detection metadata"),
    ]

    cols = st.columns(4)
    for i, (num, icon, title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center;padding:16px 8px">
              <div style="width:40px;height:40px;border-radius:12px;
                   background:linear-gradient(135deg,#4F46E5,#7C3AED);
                   display:inline-flex;align-items:center;justify-content:center;
                   color:white;font-family:'Outfit',sans-serif;font-size:18px;
                   font-weight:800;margin-bottom:10px">{num}</div>
              <div style="font-size:20px;margin-bottom:6px">{icon}</div>
              <div style="font-family:'Outfit',sans-serif;font-weight:700;
                   font-size:14px;color:#0F172A;margin-bottom:6px">{title}</div>
              <div style="font-size:12px;color:#64748B;line-height:1.5">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # CTA
    col_l, col_c, col_r = st.columns([2, 2, 2])
    with col_c:
        if st.button("🚀  Start Monitoring →", use_container_width=True):
            st.session_state.page = "monitoring"
            st.rerun()

    st.markdown("""
    <div style="text-align:center;margin-top:12px;font-size:12px;color:#94A3B8">
        Built with OpenCV · dlib · YOLOv12 · Streamlit
    </div>
    """, unsafe_allow_html=True)
