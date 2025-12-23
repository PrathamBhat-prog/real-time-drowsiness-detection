import cv2

# Shared state
from api.state import ear_value, is_drowsy, attention_state

# Existing logic (UNCHANGED imports)
from detectors.mediapipe_detector import MediaPipeFaceDetector
from detectors.features.ear import compute_ear

# New attention logic
from services.attention_service import estimate_attention


# =========================
# Configuration
# =========================
EAR_THRESHOLD = 0.25
FRAME_LIMIT = 20


def run_detector():
    counter = 0

    detector = MediaPipeFaceDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Webcam not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        landmarks = detector.detect(frame)

        if landmarks:
            h, w, _ = frame.shape

            # -------- EAR COMPUTATION --------
            ear, _ = compute_ear(landmarks, w, h)
            ear_value.value = ear

            # -------- DROWSINESS LOGIC --------
            if ear < EAR_THRESHOLD:
                counter += 1
                if counter >= FRAME_LIMIT:
                    is_drowsy.value = True
            else:
                counter = 0
                is_drowsy.value = False

            # -------- ATTENTION LOGIC --------
            attention = estimate_attention(landmarks)
            attention_state.value = attention.encode("utf-8")

        else:
            # No face detected
            ear_value.value = 0.0
            is_drowsy.value = False
            attention_state.value = b"NO_FACE"
