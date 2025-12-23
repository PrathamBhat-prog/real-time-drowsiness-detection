import cv2
from api.state import ear_value, is_drowsy

# IMPORT YOUR EXISTING MODULES (UNCHANGED)
from detectors.mediapipe_detector import MediaPipeFaceDetector
from detectors.features.ear import compute_ear


EAR_THRESHOLD = 0.25
FRAME_LIMIT = 20

def run_detector():
    counter = 0
    detector = MediaPipeFaceDetector()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        landmarks = detector.detect(frame)
        if landmarks:
            h, w, _ = frame.shape
            ear, _ = compute_ear(landmarks, w, h)

            ear_value.value = ear

            if ear < EAR_THRESHOLD:
                counter += 1
                if counter >= FRAME_LIMIT:
                    is_drowsy.value = True
            else:
                counter = 0
                is_drowsy.value = False
