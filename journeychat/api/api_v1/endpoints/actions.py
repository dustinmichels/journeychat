from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from journeychat import crud, schemas
from journeychat.api import deps
from journeychat.models.user import User
from journeychat.schemas.room import Room, RoomCreate, RoomSearchResults
from journeychat.schemas.user import UserUpdate
from sqlalchemy.orm import Session

router = APIRouter()


@router.put("/join/{room_id}", response_model=Room)
def join_room(
    *,
    room_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Join a room.
    """
    room = crud.room.get(db=db, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")

    # TODO: use crud?
    joined_rooms = [x for x in current_user.joined_rooms]
    joined_rooms.append(room)
    crud.user.update(db=db, db_obj=current_user, obj_in={"joined_rooms": joined_rooms})

    return room


@router.put("/invite/{room_id}/{username}", response_model=Room)
def add_user(
    *,
    room_id: int,
    username: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Invite a user to a room. If you are a member, they will be added immediately.
    """
    room_to_add = crud.room.get(db=db, id=room_id)
    if not room_to_add:
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")

    user_to_add = crud.user.get_by_username(db, username=username)
    if not user_to_add:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found"
        )

    if room_to_add not in current_user.joined_rooms:
        raise HTTPException(status_code=404, detail=f"Not authenticated")

    joined_rooms = [x for x in user_to_add.joined_rooms]
    joined_rooms.append(room_to_add)
    crud.user.update(db=db, db_obj=user_to_add, obj_in={"joined_rooms": joined_rooms})

    return room_to_add
