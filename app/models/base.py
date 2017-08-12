from os.path import dirname, realpath, sep
import datetime
import peewee as pw
import peewee_migrate as pwm

from app.definitions import *


def _get_database():
    database = pw.PostgresqlDatabase(database_credentials['NAME'],
                                     user=database_credentials['USER'],
                                     password=database_credentials['PASSWORD'],
                                     host=database_credentials['HOST'],
                                     port=database_credentials['PORT'])
    # Run migrations after connection established
    router = pwm.Router(database, migrate_dir=dirname(realpath(__file__)) + sep + "migrations")
    router.run()
    return database

# Deffered bare models should be set up in corresponding model files
DefferedUser = pw.DeferredRelation()
DefferedActivity = pw.DeferredRelation()
DefferedParticipant = pw.DeferredRelation()
DefferedSubscription = pw.DeferredRelation()


class _BaseModel(pw.Model):
    """ Base model, that uses PostgreSQL database """
    def __init__(self, *args, **kwargs):
        super(_BaseModel, self).__init__(*args, **kwargs)

    class Meta:
        database = _get_database()


class UserBase(_BaseModel):
    """ Telegram user, signed for bot's services """
    telegram_user_id = pw.IntegerField(primary_key=True)
    telegram_login = pw.TextField(default='')
    rights_level = pw.IntegerField(default=0)
    pending_action = pw.IntegerField(default=0)
    is_active = pw.BooleanField(default=True)
    is_disabled_chat = pw.BooleanField(default=False)

    class Meta:
        db_table = 'user'


class ActivityBase(_BaseModel):
    """ Some activity, to which users can be invited """
    name = pw.TextField(unique=True)
    owner = pw.ForeignKeyField(DefferedUser, on_delete='CASCADE')

    class Meta:
        db_table = 'activity'


class ParticipantBase(_BaseModel):
    """ User, agreed to take part in some activity """
    report_time = pw.TimestampField(default=datetime.datetime.now)
    is_accepted = pw.BooleanField(default=True)
    user = pw.ForeignKeyField(DefferedUser, on_delete='CASCADE')
    activity = pw.ForeignKeyField(DefferedActivity, on_delete='CASCADE')

    class Meta:
        db_table = 'participant'


class SubscriptionBase(_BaseModel):
    """ User, receiving notifications and able to call other users for activity """
    user = pw.ForeignKeyField(DefferedUser, on_delete='CASCADE')
    activity = pw.ForeignKeyField(DefferedActivity, on_delete='CASCADE')

    class Meta:
        db_table = 'subscription'
