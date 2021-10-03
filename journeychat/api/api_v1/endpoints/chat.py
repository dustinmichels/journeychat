from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, WebSocket

from journeychat.api import deps
from journeychat.models.user import User

import json


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    q: Optional[int] = None,
    current_user: User = Depends(deps.get_current_user_ws),
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # await websocket.send_text(f"You are: {current_user.username}")
        await websocket.send_text(f"{data} --{current_user.username}")
