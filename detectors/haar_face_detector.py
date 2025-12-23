import cv2


from detectors.base_detector import BaseFaceDetector

class HaarFaceDetector(BaseFaceDetector):
    def __init__(self, cascade_path):
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        if self.face_cascade.empty():
            raise IOError("Failed to load Haar Cascade model")

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )
        
        detections = []
        for (x, y, w, h) in faces:
            detections.append({
                "bbox": (x, y, w, h)
            })
            
        return detections

