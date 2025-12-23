import streamlit as st
import requests
import time
import collections


STATUS_URL = "http://127.0.0.1:8000/status"
METRICS_URL = "http://127.0.0.1:8000/metrics"

st.set_page_config(page_title="Drowsiness Monitor", layout="centered")
st.title("😴 Real-Time Drowsiness & Attention Monitoring")

ear_hist = collections.deque(maxlen=60)

ear_box = st.empty()
status_box = st.empty()
attention_box = st.empty()
chart_box = st.empty()
metrics_box = st.empty()

while True:
    try:
        status = requests.get(STATUS_URL, timeout=1).json()
        metrics = requests.get(METRICS_URL, timeout=1).json()

        ear = status["ear"]
        ear_hist.append(ear)

        ear_box.metric("EAR", f"{ear:.3f}")

        if status["drowsy"]:
            status_box.error("🚨 DROWSY")
        else:
            status_box.success("✅ ALERT")

        attention_box.info(f"👀 Attention: {status['attention']}")

        chart_box.line_chart(list(ear_hist))

        metrics_box.json(metrics)

    except Exception:
        st.warning("Waiting for API...")

    time.sleep(1)
