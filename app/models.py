from os.path import dirname, realpath, sep
from telegram import Bot, TelegramError
import peewee as pw
import peewee_migrate as pwm
import re
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
    telegram_login = pw.TextField(default='')
    rights_level = pw.IntegerField(default=0)
    pending_action = pw.IntegerField(default=0)
    is_active = pw.BooleanField(default=True)
    is_disabled_chat = pw.BooleanField(default=False)

    def has_right(self, command: str):
        if self.telegram_login == superuser_login:
            return True
        elif command in {'moderator_list', 'moderator_add', 'moderator_remove'}:
            return False
        elif command in {'summon', 'activity_add', 'activity_rem'}:
            return self.rights_level > 0
        return True

    def validate_info(self, login: str):
        if self.telegram_login != login or self.is_disabled_chat:
            self.telegram_login = login
            self.is_disabled_chat = False
            self.save()

    def send_message(self, bot: Bot, *args, **kwargs):
        try:
            bot.send_message(chat_id=self.telegram_user_id, *args, parse_mode='Markdown', **kwargs)
        except TelegramError:
            # User locked his conversation with bot
            self.is_disabled_chat = True
            self.save()


class Activity(_BaseModel):
    """ Some activity, to which users can be invited """
    name = pw.TextField(unique=True)
    owner = pw.ForeignKeyField(User, on_delete='CASCADE')

    @classmethod
    def try_to_create(cls, new_activity_name: str, user: User):
        max_length = 25
        new_activity_name = new_activity_name.strip()
        if len(new_activity_name) > max_length:
            return None, 'name should be no longer than *{0}* characters.'.format(max_length)
        if len(new_activity_name) == 0:
            return None, 'name is empty.'
        if not re.match("^[\w\ \_\.\-]*$", new_activity_name):
            return None, 'allowed only alphanumeric characters, spaces and `_.-`'
        if cls.select().where(cls.name == new_activity_name).count() > 0:
            return None, 'activity with name *{0}* already exists.'.format(new_activity_name)
        return cls.create(name=new_activity_name, owner=user), ''

    def has_right_to_remove(self, user: User):
        is_owner = self.owner == user
        return is_owner or user.telegram_login == superuser_login


class Participant(_BaseModel):
    """ User, agreed to take part in some activity """
    applying_time = pw.TimestampField()
    user = pw.ForeignKeyField(User, on_delete='CASCADE')
    activity = pw.ForeignKeyField(Activity, on_delete='CASCADE')


class Subscriber(_BaseModel):
    """ User, receiving notifications and able to call other users for activity """
    user = pw.ForeignKeyField(User, on_delete='CASCADE')
    activity = pw.ForeignKeyField(Activity, on_delete='CASCADE')
