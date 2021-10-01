# Import all the models, so that Base has them before being
# imported by Alembic
from journeychat.db.base_class import Base  # noqa
from journeychat.models.user import User  # noqa

# from journeychat.models.recipe import Recipe  # noqa
