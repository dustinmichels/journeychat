import asyncio
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from journeychat import crud, schemas
from journeychat.api import deps
from journeychat.models.user import User
from journeychat.schemas.room import Room, RoomCreate, RoomSearchResults
from journeychat.schemas.user import UserUpdate

router = APIRouter()


@router.get("/room/{room_id}/", response_model=List[schemas.Message])
def get_messages_for_room(
    *,
    room_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    room: Room = Depends(deps.get_room_if_member),
) -> Any:
    """
    Retrieve all messages for given rooms.
    """
    # get messages for room
    messages = crud.message.get_multi_by_room(
        db=db, room_id=room_id, skip=skip, limit=limit
    )
    return messages
