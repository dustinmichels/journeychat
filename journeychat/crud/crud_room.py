from journeychat.crud.base import CRUDBase
from journeychat.models.room import Room
from journeychat.schemas.room import RoomCreate, RoomUpdate


from sqlalchemy.orm import Session


class CRUDRoom(CRUDBase[Room, RoomCreate, RoomUpdate]):
    ...
    #  def join(self, db: Session, *, user: User) -> Optional[User]:
    #      return db.query(User).filter(User.email == email).first()


room = CRUDRoom(Room)
