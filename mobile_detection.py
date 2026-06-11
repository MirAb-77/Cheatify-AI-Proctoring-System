import cv2
import os

_model = None
_YOLO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "best_yolov12.pt")

def _load_model():
    global _model
    if _model is None:
        try:
            import torch
            from ultralytics import YOLO
            if os.path.exists(_YOLO_PATH):
                _model = YOLO(_YOLO_PATH)
                device = "cuda" if torch.cuda.is_available() else "cpu"
                _model.to(device)
        except Exception:
            _model = None

def process_mobile_detection(frame):
    _load_model()
    if _model is None:
        return frame, False
    try:
        results = _model(frame, verbose=False)
        mobile_detected = False
        for result in results:
            for box in result.boxes:
                conf = box.conf[0].item()
                cls  = int(box.cls[0].item())
                if conf < 0.8 or cls != 0:
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"Mobile ({conf:.2f})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (79, 70, 229), 3)
                cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (79, 70, 229), 2)
                mobile_detected = True
        return frame, mobile_detected
    except Exception:
        return frame, False
