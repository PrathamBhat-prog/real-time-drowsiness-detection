import cv2

from api.state import ear_value, is_drowsy, attention_state

from detectors.mediapipe_detector import MediaPipeFaceDetector
from detectors.features.ear import compute_ear
from services.attention_service import estimate_attention
from services.metrics_service import MetricsService


EAR_THRESHOLD = 0.25
FRAME_LIMIT = 20


def run_detector():
    counter = 0
    metrics = MetricsService()

    detector = MediaPipeFaceDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Webcam not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        metrics.update_fps()

        landmarks = detector.detect(frame)

        if landmarks:
            h, w, _ = frame.shape
            ear, _ = compute_ear(landmarks, w, h)

            ear_value.value = ear
            metrics.update_ear(ear)
            metrics.update_blink(ear, EAR_THRESHOLD)

            if ear < EAR_THRESHOLD:
                counter += 1
                if counter >= FRAME_LIMIT:
                    if not is_drowsy.value:
                        metrics.register_drowsy()
                    is_drowsy.value = True
            else:
                counter = 0
                is_drowsy.value = False

            attention = estimate_attention(landmarks)
            attention_state.value = attention.encode("utf-8")

        else:
            ear_value.value = 0.0
            is_drowsy.value = False
            attention_state.value = b"NO_FACE"

        # 🔑 publish metrics snapshot
        from api.state import metrics_snapshot
        metrics_snapshot.clear()
        metrics_snapshot.update(metrics.snapshot())
