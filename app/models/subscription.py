from datetime import datetime
from peewee import IntegerField, ForeignKeyField, TextField, TimestampField

from app.common import database
from app.models.activity import Activity
from app.models.user import User


class Subscription(database.BaseModel):
    # Fields.
    user = ForeignKeyField(User, on_delete='CASCADE')
    activity = ForeignKeyField(Activity, on_delete='CASCADE')

    reply_states = {
        'none': 0,
        'call': 1,
        'accept': 100,
        'accept_delayed': 101,
        'decline': 200,
    }
    reply_state = IntegerField(default=reply_states['none'])
    reply_time = TimestampField(default=datetime.now)
    reply_message = TextField(null=True)
