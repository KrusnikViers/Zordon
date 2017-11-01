from peewee import ForeignKeyField

from app.models.activity import Activity
from app.models.user import User
from app.settings import database


class ActivityAccess(database.BaseModel):
    # Fields.
    user = ForeignKeyField(User, on_delete='CASCADE')
    activity = ForeignKeyField(Activity, on_delete='CASCADE')
