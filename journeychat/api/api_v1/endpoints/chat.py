import json
from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from journeychat import crud, schemas
from journeychat.api import deps
from journeychat.models.user import User

from sqlalchemy import inspect


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: User = Depends(deps.ws_get_current_user),
    db: Session = Depends(deps.get_db),
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            # commit message to db
            json_data = json.loads(data)
            print("json_data")
            print(json_data)

            message_obj = schemas.MessageCreate(**json_data)
            print("message_obj")
            print(message_obj)

            msg_model = crud.message.create(db=db, obj_in=message_obj)
            print("msg_model")
            print(msg_model)

            msg_dict = object_as_dict(msg_model)
            print("msg_dict")
            print(msg_dict)

            response = schemas.MessageNested(**msg_dict)
            print("response")
            print(response)

            response_json = jsonable_encoder(response)
            print("response_json")
            print(response_json)

            # For future use?
            # json_data = jsonable_encoder(message_obj)
            # json_data_str = json.dumps(json_data)

            await manager.broadcast(response_json)
            # await manager.broadcast(f"{current_user.username} says: {message_obj.text}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        status_msg = dict(text=f"{current_user.username} left the chat")
        await manager.broadcast(json.dumps(status_msg))
