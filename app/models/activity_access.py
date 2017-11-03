from peewee import ForeignKeyField

from app.common import database
from app.models.activity import Activity
from app.models.user import User


class ActivityAccess(database.BaseModel):
    # Fields.
    user = ForeignKeyField(User, on_delete='CASCADE')
    activity = ForeignKeyField(Activity, on_delete='CASCADE')
