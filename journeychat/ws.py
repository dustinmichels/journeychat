# import socketio
# from socketio.exceptions import ConnectionRefusedError

# from journeychat.core.config import settings
# from fastapi import Depends
# from sqlalchemy.orm.session import Session

# from journeychat.api import deps

# # Set all CORS enabled origins
# origins = None
# if settings.BACKEND_CORS_ORIGINS:
#     origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
#     print(origins)

# sio = socketio.AsyncServer(
#     async_mode="asgi", logger=True, engineio_logger=True, cors_allowed_origins=origins
# )
# ws_app = socketio.ASGIApp(sio)


# def authenticate(token):
#     print(f"authenticating user with token {token}")
#     users = {
#         "a": {"id": 1, "username": "user-a", "joined_rooms": [1, 2, 3]},
#         "b": {"id": 2, "username": "user-b", "joined_rooms": [1, 3, 4]},
#         "c": {"id": 3, "username": "user-c", "joined_rooms": [1, 2, 4]},
#     }
#     user = users.get(token)
#     if not user:
#         raise ConnectionRefusedError("authentication failed")
#     return user


# def refresh_rooms(user, sid):
#     for room in user["joined_rooms"]:
#         print(f"Adding to room {room}")
#         sio.enter_room(sid, room)


# @sio.event
# async def connect(sid, environ, auth, i=Depends(deps.get_db)):
#     print("connect ", sid)

#     # session = await sio.get_session(sid)
#     # CONNECTIONS.append(session)
#     # authenticate user
#     # user = authenticate(auth["token"])
#     # await sio.save_session(sid, {"username": user["username"]})
#     # refresh_rooms(user, sid)
#     # print("CONNECTIONS", CONNECTIONS)


# @sio.on("chat")
# async def recieve_chat(sid, data):
#     print("message:", data)
#     room_id = int(data["room_id"])

#     # get username from session
#     session = await sio.get_session(sid)
#     data["username"] = session["username"]

#     # TODO: ensure user is authenticated for this room
#     if room_id not in sio.rooms(sid):
#         print("no access")
#         return

#     await sio.emit("chat", data, room=int(data["room_id"]))


# @sio.event
# def disconnect(sid):
#     print("disconnect ", sid)
