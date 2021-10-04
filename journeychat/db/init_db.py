import logging
from typing import List

from journeychat import crud, schemas
from journeychat.core.config import settings
from journeychat.db import base  # noqa: F401
from journeychat.initial_data import USERS, ROOMS, MESSAGES
from sqlalchemy.orm import Session

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

    # --- INIT OTHER DATA FROM FILE ---
    # Init Rooms
    for r in ROOMS:
        room_in = schemas.RoomCreate(
            name=r["name"],
            is_private=r["is_private"],
        )
        room = crud.room.create(db, obj_in=room_in)

    # Init Users
    for u in USERS:
        user_in = schemas.UserCreate(
            display_name=u["display_name"],
            email=u["email"],
            username=u["username"],
            # is_superuser=u.get("is_superuser", False),
            password=u["password"],
        )
        user = crud.user.create(db, obj_in=user_in)

    for m in MESSAGES:
        message_in = schemas.MessageCreate(
            user_id=m["user_id"],
            room_id=m["room_id"],
            timestamp=m["timestamp"],
            text=m["text"],
        )

        message = crud.message.create(db, obj_in=message_in)

        # for r in ROOMS:

        # if not user.joined_rooms:
        #     for r in ROOMS:
        #         room_in = schemas.RoomCreate(
        #             name=r["name"],
        #             is_private=r["is_private"],
        #         )
        #         room = crud.room.create(db, obj_in=room_in)

        #         # do thru crud?
        #         user.joined_rooms.append(room)

    # else:
    #     logger.warning(
    #         "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
    #         "provided as an env variable. "
    #         "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
    #     )
