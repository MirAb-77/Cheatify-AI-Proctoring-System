# Cheatify — AI-Powered Exam Proctoring System
## Streamlit Frontend

### Project Structure
```
cheatify/
├── app.py                    ← Main entry point (run this)
├── requirements.txt
├── eye_movement.py           ← Eye gaze detection module
├── head_pose.py              ← Head pose estimation module
├── mobile_detection.py       ← YOLOv12 phone detection module
│
├── models/                   ← Place model files here
│   ├── best_yolov12.pt       ← Your trained YOLO weights
│   └── shape_predictor_68_face_landmarks.dat
│
├── pages/
│   ├── landing.py            ← Home / hero page
│   ├── dashboard.py          ← Overview dashboard
│   ├── monitoring.py         ← Live webcam detection
│   ├── analytics.py          ← Plotly analytics
│   ├── evidence.py           ← Captured frames gallery
│   └── reports.py            ← Export reports
│
├── utils/
│   ├── helpers.py            ← Shared state & utilities
│   └── styles.py             ← Global CSS
│
└── evidence_gallery/         ← Auto-created, stores screenshots
```

### Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download dlib landmark model**
   ```bash
   wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
   bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
   mv shape_predictor_68_face_landmarks.dat models/
   ```

3. **Place YOLO weights**
   ```bash
   cp best_yolov12.pt models/
   ```

4. **Run**
   ```bash
   streamlit run app.py
   ```

### Features
- 🏠 **Landing Page** — Hero section, feature overview, how-it-works
- 📊 **Dashboard** — Live metrics, violation trends, risk history
- 🎥 **Live Monitoring** — Real webcam feed with all 3 modules active
- 📈 **Analytics** — Plotly charts for all detection stats
- 🖼️ **Evidence Gallery** — Auto-captured suspicious frames with download
- 📋 **Reports** — Export JSON / CSV / TXT reports

### Notes
- Detection modules require model files to be present in `models/`
- If model files are missing, the UI still works in demo mode
- All detection logic is preserved exactly from the original modules
