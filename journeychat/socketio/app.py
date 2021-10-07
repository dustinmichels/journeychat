import socketio
from socketio.exceptions import ConnectionRefusedError

from journeychat.core.config import settings


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


def refresh_rooms(user, sid):
    for room in user.joined_rooms:
        print(f"Adding to room {room.id} ({room.name})")
        sio.enter_room(sid, room.id)


@sio.event
async def connect(sid, environ, auth):
    print("> connect ", sid)

    # will return authenticated user or raise error
    user = await get_authenticated_user(auth["token"])

    # update list of rooms user is in
    refresh_rooms(user, sid)

    print(f"User {user.username} is in rooms: {sio.rooms(sid)}")

    # session = await sio.get_session(sid)
    # CONNECTIONS.append(session)
    # authenticate user
    # user = authenticate(auth["token"])
    # await sio.save_session(sid, {"username": user["username"]})
    # refresh_rooms(user, sid)
    # print("CONNECTIONS", CONNECTIONS)


@sio.on("chat")
async def recieve_chat(sid, data):
    print("message:", data)
    room_id = int(data["room_id"])

    # get username from session
    # session = await sio.get_session(sid)
    # data["username"] = session["username"]

    if room_id not in sio.rooms(sid):
        print("No access!")
        return

    await sio.emit("chat", data, room=int(data["room_id"]))


@sio.event
def disconnect(sid):
    print("disconnect ", sid)
