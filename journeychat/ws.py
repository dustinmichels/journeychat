# ws.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from journeychat.core.config import settings

ws = FastAPI()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    ws.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# websocket
@ws.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
