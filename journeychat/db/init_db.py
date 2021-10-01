import logging
from sqlalchemy.orm import Session

from journeychat import crud, schemas
from journeychat.db import base  # noqa: F401
from journeychat.core.config import settings

logger = logging.getLogger(__name__)


ROOMS = [
    {
        "name": "General",
        "is_private": False,
    },
    {
        "name": "Sci-Fi Lovers",
        "is_private": False,
    },
    {
        "name": "Python Fans",
        "is_private": False,
    },
]


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                full_name="Initial Super User",
                email=settings.FIRST_SUPERUSER,
                is_superuser=True,
                password=settings.FIRST_SUPERUSER_PW,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
        if not user.joined_rooms:
            for r in ROOMS:
                room_in = schemas.RoomCreate(
                    name=r["name"],
                    is_private=r["is_private"],
                )
                room = crud.room.create(db, obj_in=room_in)

                # link??
                user.joined_rooms.append(room)

    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
