from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from journeychat import crud, models, schemas
from journeychat.api import deps
from journeychat.models.user import User
from journeychat.schemas.room import Room, RoomCreate, RoomSearchResults
from journeychat.schemas.user import UserUpdate

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


@router.put("/{room_id}", response_model=schemas.Room)
def update_room(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.RoomUpdate,
    room: Room = Depends(deps.get_room_if_owner),
) -> Any:
    """
    Update an item.
    """
    return crud.room.update(db=db, db_obj=room, obj_in=item_in)


@router.get("/{room_id}", status_code=200, response_model=Room)
def read_room(
    *,
    room: Room = Depends(deps.get_room_if_member),
) -> Any:
    """
    Fetch a single room by ID, if public or user is member.
    """
    return room


@router.delete("/{room_id}", response_model=schemas.Room)
def delete_room(
    *,
    room_id: int,
    db: Session = Depends(deps.get_db),
    room: Room = Depends(deps.get_room_if_owner),
) -> Any:
    """
    Delete a room, if owner.
    """
    return crud.room.remove(db=db, id=room_id)


@router.get("/joined/", response_model=List[Room])
def joined_rooms(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve rooms signed-in user has joined.
    """
    return current_user.joined_rooms


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
