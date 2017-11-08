from peewee import BooleanField, IntegerField, TextField
from telegram import Bot, TelegramError

from app.common import database
from app.core import commands


class User(database.BaseModel):
    """ Telegram user, signed for bot's services """
    telegram_id = IntegerField(unique=True)
    login = TextField(default='')
    rights = IntegerField(default=0)
    mobile_layout = BooleanField(default=False)
    # Possible locale values: 'en', 'ru', 'auto'.
    locale = TextField(default='auto')

    statuses = {
        'disabled_chat': 0,
        'active': 1,
        'do_not_disturb': 2,
    }
    status = IntegerField(default=statuses['active'])

    pending_actions = {
        'none': 0,
    }
    pending_action = IntegerField(default=pending_actions['none'])

    def able(self, command_identifier) -> bool:
        return self.rights >= commands.get(command_identifier).rights_level

    def send_message(self, bot: Bot, *args, **kwargs):
        try:
            bot.send_message(self.telegram_id, *args, **kwargs)
        except TelegramError:
            self.status = self.statuses['disabled_chat']
            self.save()
