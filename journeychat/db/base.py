# Import all the models, so that Base has them before being
# imported by Alembic
from journeychat.db.base_class import Base
from journeychat.models import User, Room, Joined_Rooms, Message
