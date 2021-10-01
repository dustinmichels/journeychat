# Import all the models, so that Base has them before being
# imported by Alembic
from journeychat.db.base_class import Base
from journeychat.models.user import User
from journeychat.models.room import Room
from journeychat.models.user_rooms import User_Rooms
