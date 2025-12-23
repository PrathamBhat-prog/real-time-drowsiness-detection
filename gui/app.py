import streamlit as st
import requests
import time
import pandas as pd
import streamlit.components.v1 as components

# =========================
# Configuration
# =========================
STATUS_URL = "http://127.0.0.1:8000/status"
METRICS_URL = "http://127.0.0.1:8000/metrics"

st.set_page_config(page_title="Drowsiness Monitor", layout="centered")
st.title("😴 Real-Time Drowsiness & Attention Monitoring")

# =========================
# Live Video Stream
# =========================
st.markdown("### Live Video Feed")
components.html(
    """
    <div style="display: flex; flex-direction: column; align-items: center;">
        <img id="video" width="640" style="border: 2px solid #ccc; border-radius: 8px; background-color: #000;" />
        <div id="status" style="margin-top: 5px; color: gray; font-family: sans-serif; font-size: 12px;">Connecting...</div>
    </div>
    <script>
        const img = document.getElementById("video");
        const status = document.getElementById("status");
        
        function connect() {
            const ws = new WebSocket("ws://127.0.0.1:8000/ws/video");
            ws.binaryType = "blob";

            ws.onopen = () => {
                status.textContent = "Connected";
                status.style.color = "green";
            };

            ws.onmessage = (event) => {
                img.src = URL.createObjectURL(event.data);
            };

            ws.onclose = () => {
                status.textContent = "Disconnected. Retrying...";
                status.style.color = "red";
                setTimeout(connect, 2000);
            };

            ws.onerror = (err) => {
                status.textContent = "Error connecting to stream.";
                status.style.color = "red";
                ws.close();
            };
        }
        
        connect();
    </script>
    """,
    height=550
)

# =========================
# Metrics & Chart Prep
# =========================
if "ear_history" not in st.session_state:
    st.session_state.ear_history = []
    st.session_state.start_time = time.time()

ear_box = st.empty()
status_box = st.empty()
attention_box = st.empty()
chart_box = st.empty()
metrics_box = st.empty()

# =========================
# Main Loop
# =========================
while True:
    try:
        status_resp = requests.get(STATUS_URL, timeout=1).json()
        metrics_resp = requests.get(METRICS_URL, timeout=1).json()

        ear = status_resp["ear"]
        current_time = time.time() - st.session_state.start_time

        # Update History
        st.session_state.ear_history.append({
            "Time (seconds)": float(f"{current_time:.1f}"),
            "EAR Ratio": ear
        })
        
        # Keep last 60 points
        if len(st.session_state.ear_history) > 60:
            st.session_state.ear_history.pop(0)

        # Update Metrics UI
        ear_box.metric("EAR", f"{ear:.3f}")

        attention = status_resp['attention']
        
        if attention == "NO_FACE":
             status_box.warning("⚠️ FACE NOT DETECTED")
             attention_box.warning("⚠️ NO FACE")
        elif status_resp["drowsy"]:
            status_box.error("🚨 DROWSY")
            attention_box.error("🚨 DROWSY")
        else:
            status_box.success("✅ ALERT")
            attention_box.success(f"👀 {attention}")

        # Explanation
        explanation = status_resp.get("explanation", "Initializing...")
        st.info(f"💡 Analysis: {explanation}")

        # Update Chart with DataFrame
        df = pd.DataFrame(st.session_state.ear_history)
        if not df.empty:
            import altair as alt
            chart = alt.Chart(df.reset_index()).mark_line().encode(
                x='Time (seconds)',
                y='EAR Ratio',
                tooltip=['Time (seconds)', 'EAR Ratio']
            ).properties(
                title='EAR over Time'
            )
            chart_box.altair_chart(chart, use_container_width=True)

        metrics_box.json(metrics_resp)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        time.sleep(1)
    
    time.sleep(1)
