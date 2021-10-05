import logging

from sqlalchemy.orm import Session

from journeychat import crud, schemas
from journeychat.core.config import settings
from journeychat.db import base  # noqa: F401
from journeychat.initial_data import MESSAGES, ROOMS, USERS

logger = logging.getLogger(__name__)


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Create super user based on settings
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                display_name="Initial Super User",
                email=settings.FIRST_SUPERUSER,
                username=settings.FIRST_SUPERUSER_USERNAME,
                is_superuser=True,
                password=settings.FIRST_SUPERUSER_PW,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )

    # Init Users
    users = []
    for u in USERS:
        user_in = schemas.UserCreate(**u)
        user = crud.user.create(db, obj_in=user_in)
        users.append(user)

    # Init Rooms
    rooms = []
    for r in ROOMS:
        room_in = schemas.RoomCreate(**r)
        room = crud.room.create_with_owner(
            db, obj_in=room_in, owner_id=r.get("owner_id", 1)
        )
        rooms.append(room)

    # Add all users to the first room
    for user in users:
        crud.room.add_member(db=db, room=rooms[0], user=user)

    # Add some messages
    for m in MESSAGES:
        message_in = schemas.MessageCreate(
            user_id=m["user_id"],
            room_id=m["room_id"],
            timestamp=m["timestamp"],
            text=m["text"],
        )
        _ = crud.message.create(db, obj_in=message_in)
