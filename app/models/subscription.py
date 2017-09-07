from peewee import ForeignKeyField

from app.models.activity import Activity
from app.models.base import BaseModel
from app.models.user import User


class Subscription(BaseModel):
    """ User, receiving notifications and able to call other users for activity """
    user = ForeignKeyField(User, on_delete='CASCADE')
    activity = ForeignKeyField(Activity, on_delete='CASCADE')
