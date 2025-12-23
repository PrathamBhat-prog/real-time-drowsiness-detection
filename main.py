import cv2

from detectors.mediapipe_detector import MediaPipeFaceDetector
from detectors.features.ear import compute_ear


EAR_THRESHOLD = 0.25
FRAME_LIMIT = 20

counter = 0

face_detector = MediaPipeFaceDetector()
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Webcam not accessible")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    landmarks = face_detector.detect(frame)

    if landmarks:
        h, w, _ = frame.shape
        ear, eye_points = compute_ear(landmarks, w, h)

        for (x, y) in eye_points:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        if ear < EAR_THRESHOLD:
            counter += 1
            if counter >= FRAME_LIMIT:
                cv2.putText(
                    frame,
                    "DROWSY!",
                    (200, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 0, 255),
                    3
                )
        else:
            counter = 0

        cv2.putText(
            frame,
            f"EAR: {ear:.2f}",
            (30, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

    cv2.imshow("Drowsiness Detection (MediaPipe)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
