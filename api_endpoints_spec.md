# API Endpoints spec

## AUTH

- `/auth/login` (POST)
- `/auth/signup` (POST)
- `/auth/me` (GET)

## ROOMS

- `/rooms/` (GET)
  - List all rooms that are not private
- `/rooms/` (POST)
  - Create a new room
  - Request body: `name`, `is_private`
- `/rooms/joined` (GET)
  - List rooms the current user has joined
- `/rooms/{room_id}` (GET)
  - Get info about specific room
- `/rooms/{room_id}` (PUT)
  - Update specific room, if owner
- `/rooms/{room_id}` (DELETE)
  - Delete specific room, if owner

## Invite

- `/invite/` (POST)
  - request body: `user_id`, `room_id`

## Messages

- `/messages/room/{room_id}` (GET)
  - Get messages for particular room

## WebSockets

Send messages to:
`ws://localhost:8000/api/v1/ws?token=`

## Notes

- When you create a room you are added to it, and made the owner
- You can only edit/delete room if you are the owner
- You can invite someone to a room if you are already in it.

```

```
