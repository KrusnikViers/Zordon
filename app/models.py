import peewee as pw
from definitions import database_credentials as db_credentials

_database = pw.PostgresqlDatabase(db_credentials['NAME'],
                                  user=db_credentials['USER'],
                                  password=db_credentials['PASSWORD'],
                                  host=db_credentials['HOST'],
                                  port=db_credentials['PORT'])


class _BaseModel(pw.Model):
    """ Base model, that uses PostgreSQL database """
    def __init__(self):
        pass

    class Meta:
        database = _database


class User(_BaseModel):
    """ Telegram user, signed for bot's services """
    telegram_id = pw.IntegerField(primary_key=True)
    dnd_start_time = pw.TimeField(null=True)
    dnd_end_time = pw.TimeField(null=True)
    is_active = pw.BooleanField()


class Activity(_BaseModel):
    """ Some activity, to which users can be invited """
    name = pw.TextField(unique=True)


class Participant(_BaseModel):
    """ User, agreed to take part in some activity """
    applying_time = pw.TimestampField(null=False)
    user = pw.ForeignKeyField(User)
    activity = pw.ForeignKeyField(Activity)


class Subscriber(_BaseModel):
    """ User, receiving notifications and able to call other users for activity """
    user = pw.ForeignKeyField(User)
    activity = pw.ForeignKeyField(Activity)
