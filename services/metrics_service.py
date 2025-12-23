import time
import collections
import statistics


class MetricsService:
    def __init__(self, window_size=60):
        self.ear_window = collections.deque(maxlen=window_size)

        self.blink_count = 0
        self.drowsy_count = 0

        self.eye_closed_start = None
        self.closure_durations = []

        self.frame_count = 0
        self.start_time = time.time()

    # =========================
    # EAR metrics
    # =========================
    def update_ear(self, ear):
        self.ear_window.append(ear)

    def ear_mean(self):
        return round(statistics.mean(self.ear_window), 3) if self.ear_window else 0.0

    def ear_variance(self):
        return round(statistics.pvariance(self.ear_window), 5) if len(self.ear_window) > 1 else 0.0

    # =========================
    # Blink metrics
    # =========================
    def update_blink(self, ear, threshold):
        if ear < threshold and self.eye_closed_start is None:
            self.eye_closed_start = time.time()

        elif ear >= threshold and self.eye_closed_start is not None:
            duration = time.time() - self.eye_closed_start
            self.closure_durations.append(duration)
            self.blink_count += 1
            self.eye_closed_start = None

    def avg_closure_duration(self):
        if not self.closure_durations:
            return 0.0
        return round(sum(self.closure_durations) / len(self.closure_durations), 3)

    # =========================
    # Drowsiness
    # =========================
    def register_drowsy(self):
        self.drowsy_count += 1

    # =========================
    # Performance
    # =========================
    def update_fps(self):
        self.frame_count += 1

    def fps(self):
        elapsed = time.time() - self.start_time
        return round(self.frame_count / elapsed, 2) if elapsed > 0 else 0.0

    # =========================
    # Export metrics
    # =========================
    def snapshot(self):
        return {
            "ear_mean": self.ear_mean(),
            "ear_variance": self.ear_variance(),
            "blink_count": self.blink_count,
            "avg_eye_closure_sec": self.avg_closure_duration(),
            "drowsy_events": self.drowsy_count,
            "fps": self.fps()
        }
