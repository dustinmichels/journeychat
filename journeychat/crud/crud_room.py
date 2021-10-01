from journeychat.crud.base import CRUDBase
from journeychat.models.room import Room
from journeychat.schemas.room import RoomCreate, RoomUpdate


class CRUDRoom(CRUDBase[Room, RoomCreate, RoomUpdate]):
    ...


room = CRUDRoom(Room)
