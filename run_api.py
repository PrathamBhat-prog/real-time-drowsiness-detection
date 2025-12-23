import multiprocessing
import uvicorn
from services.detector_service import run_detector

if __name__ == "__main__":
    detector_process = multiprocessing.Process(target=run_detector)
    detector_process.start()

    uvicorn.run(
        "api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )
