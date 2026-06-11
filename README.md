<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>
<img src="https://img.shields.io/badge/YOLOv12-00FFFF?style=for-the-badge&logo=yolo&logoColor=black"/>
<img src="https://img.shields.io/badge/dlib-008000?style=for-the-badge&logoColor=white"/>
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>

<br/><br/>

# 🎓 Cheatify — AI-Powered Exam Proctoring System

**Real-time cheating surveillance with a premium multi-page Streamlit dashboard**

*Eye Gaze Tracking · Head Pose Estimation · Mobile Phone Detection · Live Risk Scoring · Evidence Gallery · PDF Reports*

<br/>

[▶ Run Demo](#-quick-start) · [📸 Screenshots](#-screenshots) · [📖 Documentation](#-how-it-works) · [🤝 Contributing](#-contributing)

</div>

---

## 📌 Overview

**Cheatify** is a production-quality AI-powered proctoring platform that detects suspicious behaviour during online exams and interviews in real time. It wraps three independent computer vision detection engines inside a polished **Streamlit web dashboard** — suitable for academic demonstrations, FYP presentations, portfolio showcases, and competition submissions.

The system runs three parallel detection modules on every webcam frame:

| Module | Technology | Detects |
|--------|-----------|---------|
| 👁️ **Eye Gaze Tracker** | dlib 68-point landmarks | Looking Left / Right / Up / Down / Center |
| 🧠 **Head Pose Estimator** | OpenCV PnP solving | Head turned beyond safe thresholds |
| 📱 **Mobile Phone Detector** | YOLOv12 (custom-trained) | Mobile device in camera frame (conf ≥ 0.80) |

---

## 🖥️ Frontend — Streamlit Dashboard

The frontend is a **6-page multi-tab Streamlit application** built with custom CSS (glassmorphism, Outfit/Inter fonts, `#4F46E5` primary palette) and Plotly charts.

### Pages at a Glance

```
app.py  ←  Entry point & sidebar navigation
│
├── 🏠  Landing Page       Hero section · Feature cards · How-it-works · CTA
├── 📊  Dashboard          Live metrics · Violation trends · Risk history · Events
├── 🎥  Live Monitoring    Webcam feed · All 3 modules · Risk gauge · Timeline
├── 📈  Analytics          5 Plotly charts · Eye / Head / Mobile / Risk breakdown
├── 🖼️  Evidence Gallery   Auto-captured frames · Confidence scores · Download
└── 📋  Reports            Behaviour analysis · Export JSON / CSV / TXT
```

### Key UI Features

- **Glassmorphism cards** with soft gradient accents
- **Live risk gauge** (Plotly indicator) that updates every frame
- **Animated calibration banner** — 5-second head-pose calibration period mirroring `main.py`
- **Auto-screenshot evidence** saved to `evidence_gallery/` on every alert trigger
- **Export system** — one-click JSON, CSV, and plain-text report download
- Fully **responsive sidebar** with module status indicators and live session metadata

---

## 📸 Screenshots

> Below are previews of the six dashboard pages.

| Landing Page | Live Dashboard |
|:---:|:---:|
| Hero · Feature cards · CTA | Metrics · Charts · Events feed |

| Live Monitoring | Analytics |
|:---:|:---:|
| Webcam feed · Detection cards · Risk gauge | 5 Plotly charts · Eye / Head / Risk |

| Evidence Gallery | Reports |
|:---:|:---:|
| Auto-captured frames · Confidence badges | Behaviour analysis · Export buttons |

---

## 📂 Project Structure

```
cheatify/
│
├── app.py                        ← Streamlit entry point & sidebar router
│
├── pages/
│   ├── landing.py                ← Hero section, feature overview, CTA
│   ├── dashboard.py              ← Metrics, charts, recent events
│   ├── monitoring.py             ← Live webcam + all 3 detection modules
│   ├── analytics.py              ← 5 Plotly analytics charts
│   ├── evidence.py               ← Captured frame gallery + download
│   └── reports.py                ← Report generation + JSON/CSV/TXT export
│
├── utils/
│   ├── helpers.py                ← Session state, risk scoring, HTML helpers
│   └── styles.py                 ← Global CSS (glassmorphism, fonts, layout)
│
├── eye_movement.py               ← Eye gaze detection module
├── head_pose.py                  ← Head pose estimation module
├── mobile_detection.py           ← YOLOv12 phone detection module
├── main.py                       ← Original standalone detection entry point
│
├── models/
│   ├── best_yolov12.pt           ← Custom-trained YOLO weights (place here)
│   └── shape_predictor_68_face_landmarks.dat  ← dlib landmark model
│
├── evidence_gallery/             ← Auto-created; stores violation screenshots
├── logs/                         ← Legacy log directory
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8+
- pip
- Webcam (for live monitoring)
- Virtual environment (recommended)

### 1 — Clone the Repository

```bash
git clone https://github.com/Sania-hasann/Cheating-Surveillance-System.git
cd Cheating-Surveillance-System
```

### 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary>Core dependencies</summary>

```
streamlit>=1.32.0
opencv-python>=4.8.0
dlib>=19.24.0
numpy>=1.24.0
pandas>=2.0.0
plotly>=5.18.0
torch>=2.0.0
torchvision>=0.15.0
ultralytics>=8.0.0
Pillow>=10.0.0
```
</details>

### 3 — Download the dlib Landmark Model

```bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
mv shape_predictor_68_face_landmarks.dat models/
```

### 4 — Add YOLO Weights

Place your trained weights inside `models/`:

```bash
cp best_yolov12.pt models/
```

> If model files are missing, the UI still runs in **demo mode** — all pages remain functional with simulated detection data.

---

## 🚀 Quick Start

### Run the Streamlit Dashboard (recommended)

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

### Run the Original CLI Pipeline

```bash
python main.py
```

The webcam opens full-screen, and detection runs in a single OpenCV window.

---

## 🧠 How It Works

### Detection Pipeline

```
        Webcam Frame (30fps)
               │
               ▼
   ┌───────────────────────────┐
   │  dlib Face Detector       │
   │  + 68-point Landmarks     │
   └───────────┬───────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
  Eye Gaze      Head Pose
  Tracking      Estimation
  (pupil pos)   (PnP solve)
        │             │
        └──────┬──────┘
               │
               ▼
   ┌───────────────────────────┐
   │  YOLOv12 Object Detector  │
   │  (Mobile Phone Detection) │
   └───────────────────────────┘
               │
               ▼
     Risk Score Engine
     (weighted combination)
               │
        ┌──────┴──────┐
        ▼             ▼
    Alert +       Evidence
    Event Log     Screenshot
```

### Risk Score Formula

```
Risk Score = min(
    eye_deviation  × 25  +
    head_movement  × 30  +
    mobile_detected × 45,
    100
)
```

| Score | Level | Action |
|-------|-------|--------|
| 0–29 | 🟢 Low | Normal behaviour |
| 30–59 | 🟡 Medium | Monitor closely |
| 60–79 | 🔴 High | Flag for review |
| 80–100 | 🚨 Critical | Immediate intervention |

### Alert & Screenshot Logic

Mirrors the logic in `main.py` exactly:

- **Eye deviation** → screenshot after **3 seconds** of continuous deviation  
- **Head movement** → screenshot after **3 seconds** beyond threshold  
- **Mobile phone** → screenshot after **2 seconds** of confirmed detection  
- All screenshots are saved to `evidence_gallery/` with timestamps

### Head Pose Calibration

On session start, a 5-second calibration window captures the candidate's neutral angles (pitch / yaw / roll). All subsequent detections are relative to this baseline — preventing false positives from natural head positioning.

---

## 📊 Detection Module Details

### 👁️ Eye Gaze Tracking (`eye_movement.py`)

Uses dlib's 68-point facial landmark predictor to locate the left eye (points 36–41) and right eye (points 42–47). Pupil position is found via contour detection on a thresholded eye ROI. Gaze is classified by normalising pupil X/Y position within the eye bounding box.

```
lx_norm < 0.35  →  Looking Left
lx_norm > 0.65  →  Looking Right
ly_norm < 0.40  →  Looking Up
ly_norm > 0.60  →  Looking Down
else            →  Looking Center  ✓
```

### 🧠 Head Pose Estimation (`head_pose.py`)

Solves the Perspective-n-Point (PnP) problem using 6 facial landmarks (nose tip, chin, eye corners, mouth corners) and a predefined 3D face model. The resulting rotation matrix is decomposed into pitch, yaw, and roll Euler angles, smoothed with a 10-frame rolling mean.

```
|yaw  offset| ≤ 12°  →  Looking at Screen  ✓
yaw < offset − 15°   →  Looking Left
yaw > offset + 15°   →  Looking Right
pitch > offset + 10° →  Looking Up
pitch < offset − 10° →  Looking Down
|roll offset| > 7°   →  Tilted
```

### 📱 Mobile Phone Detection (`mobile_detection.py`)

Runs YOLOv12 inference on each frame. Only class index `0` (mobile phone) with confidence `≥ 0.80` is flagged. Bounding boxes and confidence labels are drawn directly onto the frame.

---

## 🛠 Technologies

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit, custom CSS, Plotly |
| **Face Detection** | dlib HOG face detector |
| **Landmark Mapping** | dlib 68-point Shape Predictor |
| **Eye Tracking** | OpenCV contour detection |
| **Head Pose** | OpenCV `solvePnP`, Rodrigues decomposition |
| **Object Detection** | YOLOv12 (Ultralytics) |
| **Training Data** | Roboflow Cellphone Detection Dataset |
| **Inference Backend** | PyTorch (CUDA / CPU) |
| **Data / Charts** | Pandas, NumPy, Plotly |

---

## 📦 Dataset

The mobile detection model was trained on the **Roboflow Cellphone Detection Dataset**:

🔗 [https://universe.roboflow.com/d1156414/cellphone-0aodn](https://universe.roboflow.com/d1156414/cellphone-0aodn)

---

## 🤝 Contributing

Contributions are welcome!

```bash
# 1. Fork and clone
git clone https://github.com/your-username/Cheating-Surveillance-System.git

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and commit
git commit -m "feat: add your feature"

# 4. Push and open a PR
git push origin feature/your-feature-name
```

---

## 🔐 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [dlib](http://dlib.net/) — Facial landmark detection
- [OpenCV](https://opencv.org/) — Computer vision pipeline
- [Ultralytics YOLOv12](https://github.com/ultralytics/ultralytics) — Object detection
- [Roboflow](https://roboflow.com/) — Dataset and model training
- [Streamlit](https://streamlit.io/) — Web dashboard framework

---

<div align="center">

Made with ❤️ as a Final Year Project

⭐ Star this repo if you found it useful!

</div>
