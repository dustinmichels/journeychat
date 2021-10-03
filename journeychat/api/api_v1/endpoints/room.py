import asyncio
from typing import Any, List, Optional

# import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from journeychat import crud
from journeychat.api import deps
from journeychat.schemas.room import Room, RoomCreate, RoomSearchResults
from journeychat.schemas.user import UserUpdate


from journeychat.models.user import User


router = APIRouter()


@router.get("/", response_model=List[Room])
def read_rooms(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all rooms.
    """
    # TODO: if not private
    items = crud.room.get_multi(db, skip=skip, limit=limit)
    return items


@router.get("/joined/", response_model=List[Room])
def joined_rooms(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve items.
    """
    # TODO: move to crud
    rooms = current_user.joined_rooms
    return rooms


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


# @router.get("/", response_model=List[Room])
# def read_items(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Retrieve items.
#     """
#     if crud.user.is_superuser(current_user):
#         items = crud.item.get_multi(db, skip=skip, limit=limit)
#     else:
#         items = crud.item.get_multi_by_owner(
#             db=db, owner_id=current_user.id, skip=skip, limit=limit
#         )
#     return items


@router.get("/{room_id}", status_code=200, response_model=Room)
def fetch_room(
    *,
    room_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single room by ID
    """
    result = crud.room.get(db=db, id=room_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")

    return result


@router.get("/search/", status_code=200, response_model=RoomSearchResults)
def search_rooms(
    *,
    keyword: str = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for rooms based on label keyword
    """
    rooms = crud.room.get_multi(db=db, limit=max_results)
    results = filter(lambda room: keyword.lower() in room.name.lower(), rooms)

    return {"results": list(results)}


@router.post("/", status_code=201, response_model=Room)
def create_room(*, room_in: RoomCreate, db: Session = Depends(deps.get_db)) -> dict:
    """
    Create a new room in the database.
    """
    room = crud.room.create(db=db, obj_in=room_in)

    return room
