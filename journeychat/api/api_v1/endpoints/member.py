from typing import Any, List

from fastapi import APIRouter, Depends
from journeychat import crud, schemas
from journeychat.api import deps
from journeychat.models import Room

router = APIRouter()


@router.get("/room/{room_id}/", response_model=List[schemas.User])
def get_members_for_room(
    *,
    room: Room = Depends(deps.get_room_if_member),
) -> Any:
    """
    Retrieve all members for given rooms.
    """
    return crud.room.get_members(room=room)
