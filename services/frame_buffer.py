import threading

class FrameBuffer:
    def __init__(self):
        self.lock = threading.Lock()
        self.frame = None

    def update(self, frame):
        with self.lock:
            self.frame = frame

    def get(self):
        with self.lock:
            return self.frame
