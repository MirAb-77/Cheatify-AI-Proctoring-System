import streamlit as st
import os
import datetime
from utils.helpers import PRIMARY, SECONDARY, ACCENT, SUCCESS, WARNING, DANGER


def render_evidence():
    st.markdown('<div class="page-title">Evidence Gallery</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-breadcrumb">Automatically captured frames when violations were detected</div>',
                unsafe_allow_html=True)

    evidence = st.session_state.evidence

    if not evidence:
        st.markdown("""
        <div style="background:white;border-radius:20px;padding:60px;text-align:center;
             border:2px dashed #E2E8F0;margin:20px 0">
          <div style="font-size:48px;margin-bottom:16px">🖼️</div>
          <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:700;
               color:#0F172A;margin-bottom:8px">No Evidence Captured Yet</div>
          <div style="font-size:14px;color:#64748B;max-width:360px;margin:0 auto">
            Suspicious frames are automatically saved during active monitoring sessions.
            Start a session to begin collecting evidence.
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Summary bar ──────────────────────────────────────────────────────────
    type_counts = {}
    for ev in evidence:
        t = ev["type"].split(":")[0].strip()
        type_counts[t] = type_counts.get(t, 0) + 1

    cols = st.columns(len(type_counts) + 1)
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card">
          <div class="icon-wrap" style="background:linear-gradient(135deg,{PRIMARY}22,{PRIMARY}44)">
            <span>🖼️</span>
          </div>
          <div class="metric-value" style="color:{PRIMARY}">{len(evidence)}</div>
          <div class="metric-label">Total Frames</div>
        </div>
        """, unsafe_allow_html=True)

    type_icons = {"Eye": "👁️", "Head": "🧠", "Mobile": "📱", "Mobile Phone": "📱"}
    type_colors = {"Eye": SECONDARY, "Head": WARNING, "Mobile": DANGER, "Mobile Phone": DANGER}
    for i, (t, cnt) in enumerate(type_counts.items(), 1):
        with cols[min(i, len(cols)-1)]:
            color = type_colors.get(t, ACCENT)
            icon  = type_icons.get(t, "⚠️")
            st.markdown(f"""
            <div class="metric-card">
              <div class="icon-wrap" style="background:linear-gradient(135deg,{color}22,{color}44)">
                <span>{icon}</span>
              </div>
              <div class="metric-value" style="color:{color}">{cnt}</div>
              <div class="metric-label">{t} Violations</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Filter ───────────────────────────────────────────────────────────────
    filter_col, _ = st.columns([2, 4])
    with filter_col:
        all_types = ["All"] + list(type_counts.keys())
        selected  = st.selectbox("Filter by type", all_types, label_visibility="collapsed")

    filtered = evidence if selected == "All" else [
        e for e in evidence if e["type"].startswith(selected)
    ]

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Grid display ─────────────────────────────────────────────────────────
    COLS = 3
    rows = [filtered[i:i+COLS] for i in range(0, len(filtered), COLS)]
    for row in rows:
        ev_cols = st.columns(COLS)
        for ci, ev in enumerate(row):
            with ev_cols[ci]:
                det_type = ev["type"]
                conf     = ev["confidence"]
                ts       = ev["timestamp"]
                t_key    = det_type.split(":")[0].strip()
                color    = type_colors.get(t_key, ACCENT)
                icon     = type_icons.get(t_key, "⚠️")

                st.markdown(f"""
                <div class="evidence-card">
                """, unsafe_allow_html=True)
                try:
                    st.image(ev["image"], use_container_width=True)
                except Exception:
                    st.markdown("""
                    <div style="height:160px;background:#F1F5F9;display:flex;
                         align-items:center;justify-content:center;font-size:32px">🖼️</div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                  <div class="ev-body">
                    <div class="ev-type" style="color:{color}">{icon} {det_type}</div>
                    <div style="display:flex;justify-content:space-between;align-items:center">
                      <div class="ev-time">{ts}</div>
                      <div style="background:{color}22;color:{color};padding:2px 8px;
                           border-radius:8px;font-size:11px;font-weight:600">
                        {conf:.0%}
                      </div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # Download button
                st.download_button(
                    label="⬇ Download",
                    data=ev["image"],
                    file_name=f"evidence_{t_key}_{ts.replace(':', '-').replace(' ', '_')}.jpg",
                    mime="image/jpeg",
                    use_container_width=True,
                    key=f"dl_{ts}_{ci}_{det_type}",
                )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
