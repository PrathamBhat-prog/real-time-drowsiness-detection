import cv2


class HaarEyeDetector:
    def __init__(self, cascade_path):
        self.eye_cascade = cv2.CascadeClassifier(cascade_path)

        if self.eye_cascade.empty():
            raise IOError("Failed to load Eye Haar Cascade")

    def detect_eyes(self, gray_face):
        eyes = self.eye_cascade.detectMultiScale(
            gray_face,
            scaleFactor=1.1,
            minNeighbors=5
        )
        return eyes
