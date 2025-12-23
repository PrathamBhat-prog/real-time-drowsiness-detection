from abc import ABC, abstractmethod

class BaseFaceDetector(ABC):
    @abstractmethod
    def detect(self, frame):
        """
        Detect faces in the given frame.

        Args:
            frame: Input image (BGR).

        Returns:
            list: A list of dictionaries, where each dictionary represents a detection.
                  Example: [{"bbox": (x, y, w, h), "landmarks": ...}]
        """
        pass
