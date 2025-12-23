import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/status"

st.set_page_config(
    page_title="Drowsiness Detection",
    layout="centered"
)

st.title("😴 Real-Time Drowsiness Detection")
st.markdown("Using MediaPipe + EAR + FastAPI")

ear_placeholder = st.empty()
status_placeholder = st.empty()

while True:
    try:
        response = requests.get(API_URL, timeout=1)
        data = response.json()

        ear = data.get("ear", 0.0)
        drowsy = data.get("drowsy", False)

        ear_placeholder.metric(
            label="Eye Aspect Ratio (EAR)",
            value=f"{ear:.3f}"
        )

        if drowsy:
            status_placeholder.error("🚨 DROWSY DETECTED")
        else:
            status_placeholder.success("✅ ALERT / AWAKE")

    except Exception:
        status_placeholder.warning("⚠️ Waiting for API...")

    time.sleep(1)
