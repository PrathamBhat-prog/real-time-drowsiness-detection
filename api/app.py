from fastapi import FastAPI
from api.state import ear_value, is_drowsy

app = FastAPI(title="Drowsiness Detection API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/status")
def status():
    return {
        "ear": ear_value.value,
        "drowsy": is_drowsy.value
    }
