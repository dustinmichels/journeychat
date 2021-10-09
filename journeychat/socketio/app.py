from pydantic.errors import UrlHostError
import socketio
from socketio.exceptions import ConnectionRefusedError
from sqlalchemy.orm.session import Session

from journeychat import crud, schemas
from journeychat.api import deps
from journeychat.core.config import settings
from journeychat.models.user import User
from journeychat.socketio.security import get_authenticated_user

# Set all CORS enabled origins
origins = None
if settings.BACKEND_CORS_ORIGINS:
    origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    print(origins)

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=origins,
)
ws_app = socketio.ASGIApp(sio)

CONNECTIONS = {}


def refresh_rooms(user: User, sid: str):
    for room in user.joined_rooms:
        sio.enter_room(sid, room.id)


@sio.event
async def connect(sid, environ, auth):
    print("> WS: connect ", sid)
    # will return authenticated user or raise error
    user = await get_authenticated_user(auth["token"])

    CONNECTIONS[sid] = user.username
    print(CONNECTIONS)

    # update list of rooms user is in
    refresh_rooms(user, sid)
    print(f"User {user.username} is in rooms: {sio.rooms(sid)}")


@sio.on("new-message")
async def recieve_chat(sid, data):
    print("> WS: new-message:", data)

    # parse as Pydantic object
    msg = schemas.MessageCreate(**data)

    # Add message to database
    db: Session = next(deps.get_db())
    crud.message.create(db=db, obj_in=msg)

    await sio.emit("new-message", data, room=int(data["room_id"]))


@sio.on("join-room")
async def join_room(sid, data):
    print("> WS: join-room")
    room = data["room"]
    sio.enter_room(sid, room["id"])
    await sio.emit("new-member", data)


@sio.on("leave-room")
def leave_room(sid, room_id):
    print("> WS: leave-room")
    sio.leave_room(sid, room_id)


@sio.event
def disconnect(sid):
    print("> WS disconnect", sid)
    del CONNECTIONS[sid]
    print(CONNECTIONS)
