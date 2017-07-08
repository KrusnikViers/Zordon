from os.path import dirname, realpath, sep
import peewee as pw
import peewee_migrate as pwm
from .definitions import database_credentials, superuser_login


_database = pw.PostgresqlDatabase(database_credentials['NAME'],
                                  user=database_credentials['USER'],
                                  password=database_credentials['PASSWORD'],
                                  host=database_credentials['HOST'],
                                  port=database_credentials['PORT'])
_router = pwm.Router(_database, migrate_dir=dirname(realpath(__file__)) + sep + "migrations")
_router.run()


class _BaseModel(pw.Model):
    """ Base model, that uses PostgreSQL database """
    class Meta:
        database = _database


class User(_BaseModel):
    """ Telegram user, signed for bot's services """
    telegram_user_id = pw.IntegerField(primary_key=True)
    telegram_chat_id = pw.IntegerField(unique=True)
    telegram_login = pw.TextField(default='')
    rights_level = pw.IntegerField(default=0)
    pending_action = pw.IntegerField(default=0)
    is_active = pw.BooleanField(default=True)
    is_disabled_chat = pw.BooleanField(default=False)

    def has_right(self, command: str):
        if self.telegram_login == '@' + superuser_login:
            return True
        elif command in {'activity_rem', 'moderator_list', 'moderator_add', 'moderator_remove'}:
            return False
        elif command in {'summon', 'activity_add'}:
            return self.rights_level > 0
        return True

    def validate_info(self, login: str):
        if self.telegram_login != login or self.is_disabled_chat:
            self.telegram_login = login
            self.is_disabled_chat = False
            self.save()


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
