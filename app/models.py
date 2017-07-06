from os.path import dirname, realpath, sep
import peewee as pw
import peewee_migrate as pwm
from .definitions import database_credentials

_database = pw.PostgresqlDatabase(database_credentials['NAME'],
                                  user=database_credentials['USER'],
                                  password=database_credentials['PASSWORD'],
                                  host=database_credentials['HOST'],
                                  port=database_credentials['PORT'])
_router = pwm.Router(_database, migrate_dir=dirname(realpath(__file__)) + sep + "migrations")
_router.run()


class _BaseModel(pw.Model):
    """ Base model, that uses PostgreSQL database """
    def __init__(self, *args, **kwargs):
        # Explicitly passing constructor arguments to pw.Model.
        super(_BaseModel, self).__init__(*args, **kwargs)

    class Meta:
        database = _database


class User(_BaseModel):
    """ Telegram user, signed for bot's services """
    telegram_id = pw.IntegerField(primary_key=True)
    is_active = pw.BooleanField()
    is_moderator = pw.BooleanField()


class Activity(_BaseModel):
    """ Some activity, to which users can be invited """
    name = pw.TextField(unique=True)


class Participant(_BaseModel):
    """ User, agreed to take part in some activity """
    applying_time = pw.TimestampField()
    user = pw.ForeignKeyField(User)
    activity = pw.ForeignKeyField(Activity)


class Subscriber(_BaseModel):
    """ User, receiving notifications and able to call other users for activity """
    user = pw.ForeignKeyField(User)
    activity = pw.ForeignKeyField(Activity)
