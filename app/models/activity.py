from peewee import CompositeKey, IntegerField, ForeignKeyField, TextField

from app.core.database import BaseModel
from app.models.user import User


class Activity(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()

    class Meta:
        table_name = 'activities'


class Participant(BaseModel):
    activity = ForeignKeyField(Activity)
    user = ForeignKeyField(User)

    class Meta:
        table_name = 'participants'
        primary_key = CompositeKey('activity', 'user')
