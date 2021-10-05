# API Endpoints spec

## AUTH

- `/auth/login` (POST) ✅
- `/auth/signup` (POST) ✅
- `/auth/me` (GET) ✅

## ROOMS

- `/rooms/` (GET) ✅
  - List all rooms that are not private
- `/rooms/` (POST) ✅
  - Create a new room
  - Request body:
    ```json
    { "name": "string", "is_private": true }
    ```
- `/rooms/joined` (GET) ✅
  - List rooms the current user has joined
- `/rooms/{room_id}` (GET) ✅
  - Get info about specific room, if authorized
- `/rooms/{room_id}` (PUT) ✅
  - Update specific room, if owner
- `/rooms/{room_id}` (DELETE) ✅
  - Delete specific room, if owner

## Members

- `/members/{room_id}` (GET) ❌
  - Get members for a specific room, if authenticated

## Actions

- `actions/invite/{room_id}/{username}` (PUT) ✅
  - Invite particular user to particular room
  - They will be automatically added
- `actions/join/{room_id}/` (PUT) ✅
  - Join a particular room, if public

## Messages

- `/messages/room/{room_id}` (GET) ✅
  - Get messages for particular room

## WebSockets

- `ws://.../ws?token=...`
  - Connect to websocket
- Send messages as stringified JSON:
  ```json
  { "user_id": int, "room_id": int, "timestamp": str, "text": str }
  ```

## Security Flow

- When you create a room you are added to it, and made the owner
- You can invite someone to a room if you are already in it.
- You can only edit/delete room if you are the owner
