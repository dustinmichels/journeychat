from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from journeychat import crud, schemas
from journeychat.api import deps
from journeychat.models.user import User
from journeychat.schemas.room import Room, RoomCreate, RoomSearchResults
from journeychat.schemas.user import UserUpdate
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[Room])
def read_rooms(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all public rooms.
    """
    items = crud.room.get_multi_if_public(db, skip=skip, limit=limit)
    return items


@router.post("/", status_code=201, response_model=Room)
def create_room(
    *,
    room_in: RoomCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Create a new room in the database.
    """
    room = crud.room.create_with_owner(db=db, obj_in=room_in, owner_id=current_user.id)
    return room


@router.get("/joined/", response_model=List[Room])
def joined_rooms(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve items.
    """
    return current_user.joined_rooms


@router.get("/{room_id}", status_code=200, response_model=Room)
def fetch_room(
    *,
    room: Room = Depends(deps.get_room_authenticated),
) -> Any:
    """
    Fetch a single room by ID.
    Use dependency injection to assert: must be public or user must be member.
    """
    return room


# @router.get("/search/", status_code=200, response_model=RoomSearchResults)
# def search_rooms(
#     *,
#     keyword: str = Query(None, min_length=3, example="chicken"),
#     max_results: Optional[int] = 10,
#     db: Session = Depends(deps.get_db),
# ) -> dict:
#     """
#     Search for rooms based on label keyword
#     """
#     rooms = crud.room.get_multi(db=db, limit=max_results)
#     results = filter(lambda room: keyword.lower() in room.name.lower(), rooms)

#     return {"results": list(results)}
