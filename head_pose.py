import cv2
import dlib
import numpy as np
import math
from collections import deque
import os

_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "shape_predictor_68_face_landmarks.dat")
_detector = None
_predictor = None

model_points = np.array([
    (0.0, 0.0, 0.0), (0.0, -50.0, -10.0), (-30.0, 40.0, -10.0),
    (30.0, 40.0, -10.0), (-25.0, -30.0, -10.0), (25.0, -30.0, -10.0)
], dtype=np.float64)

focal_length = 640
center = (320, 240)
camera_matrix = np.array([[focal_length,0,center[0]],[0,focal_length,center[1]],[0,0,1]], dtype=np.float64)
dist_coeffs = np.zeros((4, 1))

ANGLE_HISTORY_SIZE = 10
yaw_history   = deque(maxlen=ANGLE_HISTORY_SIZE)
pitch_history = deque(maxlen=ANGLE_HISTORY_SIZE)
roll_history  = deque(maxlen=ANGLE_HISTORY_SIZE)
previous_state = "Looking at Screen"

def _load_models():
    global _detector, _predictor
    if _detector is None:
        _detector = dlib.get_frontal_face_detector()
    if _predictor is None and os.path.exists(_MODEL_PATH):
        _predictor = dlib.shape_predictor(_MODEL_PATH)

def get_head_pose_angles(image_points):
    success, rotation_vector, _ = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    if not success:
        return None
    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    sy = math.sqrt(rotation_matrix[0,0]**2 + rotation_matrix[1,0]**2)
    singular = sy < 1e-6
    if not singular:
        pitch = math.atan2(rotation_matrix[2,1], rotation_matrix[2,2])
        yaw   = math.atan2(-rotation_matrix[2,0], sy)
        roll  = math.atan2(rotation_matrix[1,0], rotation_matrix[0,0])
    else:
        pitch = math.atan2(-rotation_matrix[1,2], rotation_matrix[1,1])
        yaw   = math.atan2(-rotation_matrix[2,0], sy)
        roll  = 0
    return np.degrees(pitch), np.degrees(yaw), np.degrees(roll)

def smooth_angle(angle_history, new_angle):
    angle_history.append(new_angle)
    return np.mean(angle_history)

def process_head_pose(frame, calibrated_angles=None):
    global previous_state
    _load_models()
    if _detector is None or _predictor is None:
        return frame, "Looking at Screen"
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = _detector(gray)
    head_direction = "Looking at Screen"
    for face in faces:
        landmarks = _predictor(gray, face)
        image_points = np.array([
            (landmarks.part(30).x, landmarks.part(30).y),
            (landmarks.part(8).x,  landmarks.part(8).y),
            (landmarks.part(36).x, landmarks.part(36).y),
            (landmarks.part(45).x, landmarks.part(45).y),
            (landmarks.part(48).x, landmarks.part(48).y),
            (landmarks.part(54).x, landmarks.part(54).y)
        ], dtype=np.float64)
        angles = get_head_pose_angles(image_points)
        if angles is None:
            continue
        pitch = smooth_angle(pitch_history, angles[0])
        yaw   = smooth_angle(yaw_history,   angles[1])
        roll  = smooth_angle(roll_history,  angles[2])
        if calibrated_angles is None:
            return frame, (pitch, yaw, roll)
        calibrated_angles = tuple(np.ravel(calibrated_angles))
        pitch_offset, yaw_offset, roll_offset = calibrated_angles[:3]
        PITCH_THRESHOLD = 8
        YAW_THRESHOLD   = 12
        ROLL_THRESHOLD  = 5
        if abs(yaw-yaw_offset)<=YAW_THRESHOLD and abs(pitch-pitch_offset)<=PITCH_THRESHOLD and abs(roll-roll_offset)<=ROLL_THRESHOLD:
            current_state = "Looking at Screen"
        elif yaw < yaw_offset - 15:
            current_state = "Looking Left"
        elif yaw > yaw_offset + 15:
            current_state = "Looking Right"
        elif pitch > pitch_offset + 10:
            current_state = "Looking Up"
        elif pitch < pitch_offset - 10:
            current_state = "Looking Down"
        elif abs(roll - roll_offset) > 7:
            current_state = "Tilted"
        else:
            current_state = previous_state
        previous_state = current_state
        head_direction = current_state
    return frame, head_direction
