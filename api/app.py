from fastapi import FastAPI
from api.state import ear_value, is_drowsy, attention_state, metrics_snapshot
from api.schemas import DrowsinessStatus

app = FastAPI(title="Drowsiness Detection API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/status", response_model=DrowsinessStatus)
def status():
    return {
        "ear": ear_value.value,
        "drowsy": is_drowsy.value,
        "attention": attention_state.value.decode("utf-8")
    }


@app.get("/metrics")
def metrics():
    return dict(metrics_snapshot)
