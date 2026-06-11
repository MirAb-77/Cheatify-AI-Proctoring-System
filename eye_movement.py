import cv2
import dlib
import numpy as np
import os

_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "shape_predictor_68_face_landmarks.dat")
_detector = None
_predictor = None

def _load_models():
    global _detector, _predictor
    if _detector is None:
        _detector = dlib.get_frontal_face_detector()
    if _predictor is None and os.path.exists(_MODEL_PATH):
        _predictor = dlib.shape_predictor(_MODEL_PATH)

def detect_pupil(eye_region):
    if eye_region.size == 0:
        return None, None
    gray_eye = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
    blurred_eye = cv2.GaussianBlur(gray_eye, (7, 7), 0)
    _, threshold_eye = cv2.threshold(blurred_eye, 50, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold_eye, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        pupil_contour = max(contours, key=cv2.contourArea)
        px, py, pw, ph = cv2.boundingRect(pupil_contour)
        return (px + pw // 2, py + ph // 2), (px, py, pw, ph)
    return None, None

def process_eye_movement(frame):
    _load_models()
    if _detector is None or _predictor is None:
        return frame, "Looking Center"
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = _detector(gray)
    gaze_direction = "Looking Center"
    for face in faces:
        landmarks = _predictor(gray, face)
        left_eye_points  = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)])
        right_eye_points = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)])
        left_eye_rect  = cv2.boundingRect(left_eye_points)
        right_eye_rect = cv2.boundingRect(right_eye_points)
        l_x, l_y, l_w, l_h = left_eye_rect
        r_x, r_y, r_w, r_h = right_eye_rect
        left_eye  = frame[l_y:l_y+l_h, l_x:l_x+l_w] if l_h>0 and l_w>0 else np.zeros((1,1,3), np.uint8)
        right_eye = frame[r_y:r_y+r_h, r_x:r_x+r_w] if r_h>0 and r_w>0 else np.zeros((1,1,3), np.uint8)
        left_pupil,  _ = detect_pupil(left_eye)
        right_pupil, _ = detect_pupil(right_eye)
        cv2.rectangle(frame, (l_x, l_y), (l_x+l_w, l_y+l_h), (79, 70, 229), 2)
        cv2.rectangle(frame, (r_x, r_y), (r_x+r_w, r_y+r_h), (79, 70, 229), 2)
        if left_pupil:
            cv2.circle(frame, (l_x+left_pupil[0], l_y+left_pupil[1]), 5, (6, 182, 212), -1)
        if right_pupil:
            cv2.circle(frame, (r_x+right_pupil[0], r_y+right_pupil[1]), 5, (6, 182, 212), -1)
        if left_pupil and right_pupil:
            lx_norm = left_pupil[0]  / max(l_w, 1)
            rx_norm = right_pupil[0] / max(r_w, 1)
            ly_norm = (left_pupil[1] / max(l_h, 1) + right_pupil[1] / max(r_h, 1)) / 2
            if lx_norm < 0.35 and rx_norm < 0.35:
                gaze_direction = "Looking Left"
            elif lx_norm > 0.65 and rx_norm > 0.65:
                gaze_direction = "Looking Right"
            elif ly_norm < 0.4:
                gaze_direction = "Looking Up"
            elif ly_norm > 0.6:
                gaze_direction = "Looking Down"
            else:
                gaze_direction = "Looking Center"
    return frame, gaze_direction
