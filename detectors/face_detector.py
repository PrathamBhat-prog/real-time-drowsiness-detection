import cv2


class FaceDetector:
    def __init__(self, cascade_path):
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        if self.face_cascade.empty():
            raise IOError("Failed to load Haar Cascade model")

    def detect_faces(self, gray_frame):
        faces = self.face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.3,
            minNeighbors=5
        )
        return faces
