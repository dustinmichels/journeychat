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
    # logger=True,
    # engineio_logger=True,
)
ws_app = socketio.ASGIApp(sio)

CONNECTIONS = {}


def refresh_rooms(user, sid):
    for room in user.joined_rooms:
        # print(f"Adding to room {room.id} ({room.name})")
        sio.enter_room(sid, room.id)


@sio.event
async def connect(sid, environ, auth):
    print("> connect ", sid)
    # will return authenticated user or raise error
    user = await get_authenticated_user(auth["token"])

    CONNECTIONS[sid] = user.username
    print(CONNECTIONS)

    # update list of rooms user is in
    refresh_rooms(user, sid)
    print(f"User {user.username} is in rooms: {sio.rooms(sid)}")

    for room in sio.rooms(sid):
        await sio.emit("online-ping", data=user.username, room=room, skip_sid=sid)

    # session = await sio.get_session(sid)
    # CONNECTIONS.append(session)
    # authenticate user
    # user = authenticate(auth["token"])
    # await sio.save_session(sid, {"username": user["username"]})
    # refresh_rooms(user, sid)


@sio.on("new-message")
async def recieve_chat(sid, data):
    print("message:", data)

    # parse as Pydantic object
    msg = schemas.MessageCreate(**data)

    # get username from session
    # session = await sio.get_session(sid)
    # data["username"] = session["username"]

    # if msg.room_id not in sio.rooms(sid):
    #     print("No access!")
    #     return

    # Add message to database
    db: Session = next(deps.get_db())
    crud.message.create(db=db, obj_in=msg)

    await sio.emit("new-message", data, room=int(data["room_id"]))


@sio.event
def disconnect(sid):
    print("disconnect ", sid)
    del CONNECTIONS[sid]
    print(CONNECTIONS)
