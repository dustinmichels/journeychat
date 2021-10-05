# API Endpoints spec

## AUTH

- `/auth/login` (POST) ✅
- `/auth/signup` (POST) ✅
- `/auth/me` (GET) ✅

## ROOMS

- `/rooms/` (GET) ❌
  - List all rooms that are not private
- `/rooms/` (POST) ❌
  - Create a new room
  - Request body:
    ```json
    { "name": "string", "is_private": true }
    ```
- `/rooms/joined` (GET)
  - List rooms the current user has joined
- `/rooms/{room_id}` (GET)
  - Get info about specific room
- `/rooms/{room_id}` (PUT) ❌
  - Update specific room, if owner
- `/rooms/{room_id}` (DELETE) ❌
  - Delete specific room, if owner

## Actions

- `actions/invite/{room_id}/{username}` (POST) ❌
  - Invite particular user to particular room
- `actions/join/{room_id}/` (POST) ❌
  - Join a particular room

## Messages

- `/messages/room/{room_id}` (GET) ❌
  - Get messages for particular room

## WebSockets

Connect to websocket:
`ws://.../ws?token=`

Send messages as stringified JSON:

```json
{ "user_id": int, "room_id": int, "text": str }
```

Either:

1. Separate web socket for each room?
2. Include room data in message

## Notes

- When you create a room you are added to it, and made the owner
- You can only edit/delete room if you are the owner
- You can invite someone to a room if you are already in it.
