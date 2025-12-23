import threading
import uvicorn
from services.detector_service import run_detector

if __name__ == "__main__":
    detector_thread = threading.Thread(
        target=run_detector,
        daemon=True
    )
    detector_thread.start()

    uvicorn.run(
        "api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )
