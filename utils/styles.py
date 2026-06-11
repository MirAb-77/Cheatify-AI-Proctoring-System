GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root & Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #0F172A;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }

/* ── Background ── */
.stApp { background: #F8FAFC; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E1B4B 0%, #312E81 50%, #4C1D95 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #E0E7FF !important; }
[data-testid="stSidebar"] .stRadio label { 
    color: #C7D2FE !important; 
    font-size: 14px;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }
[data-testid="stSidebarNav"] { display: none; }

/* ── Metric cards ── */
.metric-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    border: 1px solid #F1F5F9;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
    height: 100%;
}
.metric-card:hover {
    box-shadow: 0 4px 20px rgba(79,70,229,0.12);
    transform: translateY(-2px);
}
.metric-card .icon-wrap {
    width: 48px; height: 48px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 16px;
    font-size: 22px;
}
.metric-card .metric-value {
    font-family: 'Outfit', sans-serif;
    font-size: 36px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 6px;
}
.metric-card .metric-label {
    font-size: 13px;
    color: #64748B;
    font-weight: 500;
    letter-spacing: 0.02em;
}
.metric-card .metric-delta {
    font-size: 12px;
    margin-top: 6px;
    font-weight: 500;
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 28px;
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 4px 24px rgba(79,70,229,0.08);
}

/* ── Section header ── */
.section-header {
    font-family: 'Outfit', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 13px;
    color: #64748B;
    margin-bottom: 20px;
}

/* ── Status badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-success { background: #DCFCE7; color: #15803D; }
.badge-warning { background: #FEF9C3; color: #A16207; }
.badge-danger  { background: #FEE2E2; color: #DC2626; }
.badge-info    { background: #EFF6FF; color: #1D4ED8; }
.badge-purple  { background: #F3F4FF; color: #4F46E5; }

/* ── Detection status card ── */
.detection-card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #F1F5F9;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.detection-card.alert-active {
    border-color: #FECACA;
    background: linear-gradient(135deg, #FFF5F5 0%, #FFFBFB 100%);
    box-shadow: 0 0 0 3px rgba(239,68,68,0.1);
}
.detection-card.warning-active {
    border-color: #FDE68A;
    background: linear-gradient(135deg, #FFFBEB 0%, #FFFDF5 100%);
    box-shadow: 0 0 0 3px rgba(245,158,11,0.1);
}
.detection-card .card-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 14px;
    color: #374151;
    margin-bottom: 8px;
}
.detection-card .card-status {
    font-size: 22px;
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
}

/* ── Timeline ── */
.timeline-item {
    display: flex;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #F1F5F9;
    align-items: flex-start;
}
.timeline-item:last-child { border-bottom: none; }
.timeline-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-top: 6px;
    flex-shrink: 0;
}
.timeline-time {
    font-family: 'Inter', monospace;
    font-size: 11px;
    color: #94A3B8;
    white-space: nowrap;
    min-width: 70px;
}
.timeline-msg {
    font-size: 13px;
    color: #374151;
    line-height: 1.4;
}

/* ── Risk gauge wrapper ── */
.risk-wrap {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #F1F5F9;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    text-align: center;
}

/* ── Page title ── */
.page-title {
    font-family: 'Outfit', sans-serif;
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 2px;
}
.page-breadcrumb {
    font-size: 13px;
    color: #94A3B8;
    margin-bottom: 24px;
}

/* ── Video container ── */
.video-container {
    border-radius: 16px;
    overflow: hidden;
    border: 2px solid #E2E8F0;
    background: #0F172A;
}

/* ── Alert items ── */
.alert-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-size: 13px;
    border-left: 3px solid;
}
.alert-danger { background: #FFF5F5; border-left-color: #EF4444; }
.alert-warning { background: #FFFBEB; border-left-color: #F59E0B; }
.alert-info { background: #EFF6FF; border-left-color: #3B82F6; }
.alert-success { background: #F0FDF4; border-left-color: #22C55E; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(79,70,229,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(79,70,229,0.4) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #F1F5F9;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 500;
    color: #64748B;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #4F46E5 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

/* ── Divider ── */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #E2E8F0, transparent);
    margin: 20px 0;
}

/* ── Evidence card ── */
.evidence-card {
    background: white;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #F1F5F9;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s ease;
}
.evidence-card:hover {
    box-shadow: 0 4px 20px rgba(79,70,229,0.12);
}
.evidence-card .ev-body {
    padding: 14px;
}
.evidence-card .ev-type {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.evidence-card .ev-time {
    font-family: 'Inter', monospace;
    font-size: 12px;
    color: #64748B;
}

/* ── Landing specific ── */
.landing-hero {
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 40%, #4C1D95 70%, #6D28D9 100%);
    border-radius: 24px;
    padding: 60px 40px;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.landing-hero::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at center, rgba(124,58,237,0.3) 0%, transparent 60%);
    animation: hero-pulse 4s ease-in-out infinite;
}
@keyframes hero-pulse {
    0%,100%{transform:scale(1);opacity:0.6;}
    50%{transform:scale(1.1);opacity:1;}
}
.landing-title {
    font-family: 'Outfit', sans-serif;
    font-size: 56px;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 16px;
    position: relative;
}
.landing-sub {
    font-size: 18px;
    color: rgba(255,255,255,0.75);
    max-width: 500px;
    margin: 0 auto 32px;
    line-height: 1.6;
    position: relative;
}

/* ── Sidebar nav item ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.15s;
    color: #C7D2FE;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 2px;
}
.nav-item:hover { background: rgba(255,255,255,0.1); }
.nav-item.active { background: rgba(255,255,255,0.15); color: white; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
</style>
"""
