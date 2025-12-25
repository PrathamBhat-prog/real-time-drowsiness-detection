# 💤 Real-Time Drowsiness and Attention Detection System

This project implements a **real-time computer vision system** that monitors a user through a webcam to detect **drowsiness and attentiveness**.  
It uses **facial landmarks**, **Eye Aspect Ratio (EAR)**, and **head orientation** to analyze eye closure patterns and attention state.

The system is built as a **complete end-to-end pipeline**, combining:
- real-time computer vision inference,
- a backend API using **FastAPI**,
- live metrics computation,
- **WebSocket-based video streaming**, and
- a **Streamlit-based GUI** for visualization.

---

## 📌 Key Features

- 🎥 Real-time webcam-based face analysis
- 👁️ Eye Aspect Ratio (EAR) computation using facial landmarks
- 😴 Drowsiness detection based on sustained eye closure
- 👀 Attention detection using head orientation
- 💡 Minimal, rule-based explainability for decisions
- ⚡ FastAPI backend exposing live state and metrics
- 📊 Live in-memory metrics (EAR statistics, blink count, FPS)
- 🔁 WebSocket-based live video streaming with overlays
- 🖥️ Streamlit dashboard for real-time monitoring

---

## 🧠 System Overview

The system continuously captures frames from a webcam using OpenCV and extracts facial landmarks using **MediaPipe Face Mesh**.

From these landmarks:
- Eye landmarks are used to compute **Eye Aspect Ratio (EAR)**.
- EAR values are tracked over time to detect prolonged eye closure.
- Relative facial landmark positions are used to estimate **head orientation**, indicating attentiveness or distraction.

The computer vision loop runs independently and updates shared state variables.  
These states are then consumed by:
- REST API endpoints for structured data,
- a WebSocket endpoint for live annotated video streaming, and
- a Streamlit GUI for human-readable visualization.

---

## 🔍 Drowsiness Detection Logic

Drowsiness detection is based on the **Eye Aspect Ratio (EAR)**, a numerical measure of eye openness.

### Detection Process
1. EAR is computed for each frame using eye landmarks.
2. A fixed threshold separates open and closed eye states.
3. If EAR remains below the threshold for a predefined number of consecutive frames, the system marks the user as **drowsy**.
4. When EAR returns above the threshold, the system resets to an alert state.

This temporal approach prevents false positives caused by natural blinking.

---

## 👀 Attention Detection Logic

Attention is estimated using **relative facial landmark geometry**:

- The position of the nose is compared with the midpoint between the eyes.
- A significant horizontal deviation indicates the head is turned away.
- The system classifies attention as:
  - `ATTENTIVE`
  - `LOOKING_AWAY`
  - `NO_FACE` (if no face is detected)

---

## 💡 Minimal Explainability

The system includes **minimal, rule-based explainability** to clarify why a particular state is reported.

For every frame, a **human-readable explanation** is generated, such as:
- `Drowsiness detected! EAR < threshold`
- `Distracted: Looking away`
- `Eye openness within normal range`
- `No face detected`

This explanation is:
- stored in shared state,
- returned by the `/status` API endpoint, and
- displayed in the Streamlit GUI under an analysis section.

The explanations are derived directly from the same signals used for detection, ensuring transparency and consistency.

---

## 🔒 State Consistency Handling

To avoid conflicting or confusing outputs, the system enforces **state consistency rules**:

- If **drowsiness is detected**, the attention state is overridden to `"DROWSY"`.
- If **no face is detected**, the GUI prioritizes `"FACE NOT DETECTED"` over alert states.
- Only one dominant state is presented to the user at any time.

---

## 📊 Live Metrics

The system computes **live, in-memory metrics** during runtime, including:

- Mean EAR (rolling window)
- EAR variance
- Blink count
- Average eye-closure duration
- Drowsiness event count
- Frames Per Second (FPS)

Metrics are updated continuously and reset automatically when the application restarts.

---

## 🌐 API Interface (FastAPI)

### Health Check

GET /health

### Current Detection State

GET /status

**Sample Response**
json
{
  "ear": 0.28,
  "drowsy": false,
  "attention": "ATTENTIVE",
  "explanation": "Eye openness within normal range"
}

---

## WebSocket Video Streaming

The system supports live video streaming via WebSockets.

Webcam frames are annotated with EAR value, attention state, and drowsiness alerts.

Frames are streamed in real time to a browser-based client.

The WebSocket server runs alongside the REST API within the same FastAPI application.

This enables real-time visualization without relying on OpenCV GUI windows.

---

## Streamlit Dashboard

The Streamlit GUI provides a real-time dashboard that displays:

Current EAR value

Drowsiness status

Attention state

Human-readable explanation of the current state

EAR time-series graph

Live metrics output

The GUI consumes data directly from the FastAPI backend.

---

### Tech Stack

Python

OpenCV

MediaPipe

FastAPI

WebSockets

Streamlit

NumPy

---

### How to Run the Project

1. Clone the Repository

git clone https://github.com/PrathamBhat-prog/real-time-drowsiness-detection.git
cd real-time-drowsiness-detection

2. Create and Activate Virtual Environment

python -m venv venv
venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Start Backend (CV + API + WebSocket)

python run_api_threaded.py

5. Start Streamlit GUI

streamlit run gui/app.py

