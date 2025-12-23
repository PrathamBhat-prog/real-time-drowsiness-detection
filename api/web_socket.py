import cv2
import asyncio
from fastapi import WebSocket
from services.detector_service import frame_buffer


async def video_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            frame = frame_buffer.get()
            if frame is None:
                await asyncio.sleep(0.03)
                continue

            _, buffer = cv2.imencode(".jpg", frame)
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.03)

    except Exception:
        await websocket.close()
