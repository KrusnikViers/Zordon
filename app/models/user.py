from peewee import IntegerField, TextField
from telegram import Bot, TelegramError

from app.settings import database


class User(database.BaseModel):
    """ Telegram user, signed for bot's services """
    telegram_id = IntegerField(unique=True)
    login = TextField(default='')
    rights = IntegerField(default=0)

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

    def send_message(self, bot: Bot, *args, **kwargs):
        try:
            bot.send_message(self.telegram_id, *args, **kwargs)
        except TelegramError:
            self.status = self.statuses['disabled_chat']
            self.save()
