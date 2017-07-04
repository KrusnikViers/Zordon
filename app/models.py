import peewee as pw
import definitions as defines

_database = pw.PostgresqlDatabase(defines.db_name, user=defines.db_user, password=defines.db_pass, host=defines.db_host)


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

# Create models, if necessary
_database.create_tables([User, Activity, Participant], safe=True)
