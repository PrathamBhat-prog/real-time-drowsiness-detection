import streamlit as st
import requests
import time
import collections


# =========================
# Configuration
# =========================
API_URL = "http://127.0.0.1:8000/status"
REFRESH_INTERVAL = 1  # seconds
MAX_POINTS = 60       # EAR history length


# =========================
# Streamlit Page Setup
# =========================
st.set_page_config(
    page_title="Real-Time Drowsiness & Attention Monitoring",
    layout="centered"
)

st.title("😴 Real-Time Drowsiness & Attention Monitoring")
st.markdown(
    "MediaPipe + EAR + Attention Detection  \n"
    "Backend: FastAPI | Frontend: Streamlit"
)

st.divider()


# =========================
# UI Placeholders
# =========================
ear_metric = st.empty()
drowsy_status = st.empty()
attention_status = st.empty()
ear_chart = st.empty()
error_box = st.empty()


# =========================
# EAR History Buffer
# =========================
ear_history = collections.deque(maxlen=MAX_POINTS)


# =========================
# Main Update Loop
# =========================
while True:
    try:
        response = requests.get(API_URL, timeout=1)
        data = response.json()

        ear = data.get("ear", 0.0)
        drowsy = data.get("drowsy", False)
        attention = data.get("attention", "UNKNOWN")

        # Update EAR metric
        ear_metric.metric(
            label="Eye Aspect Ratio (EAR)",
            value=f"{ear:.3f}"
        )

        # Update drowsiness status
        if drowsy:
            drowsy_status.error("🚨 DROWSY DETECTED")
        else:
            drowsy_status.success("✅ ALERT / AWAKE")

        # Update attention status
        if attention == "ATTENTIVE":
            attention_status.success("👀 ATTENTIVE")
        elif attention == "LOOKING_AWAY":
            attention_status.warning("⚠️ LOOKING AWAY")
        elif attention == "NO_FACE":
            attention_status.error("❌ NO FACE DETECTED")
        else:
            attention_status.info("ℹ️ ATTENTION UNKNOWN")

        # Update EAR history & chart
        ear_history.append(ear)
        ear_chart.line_chart(list(ear_history))

        error_box.empty()

    except Exception as e:
        error_box.warning("⚠️ Waiting for API connection...")
        time.sleep(REFRESH_INTERVAL)
        continue

    time.sleep(REFRESH_INTERVAL)
