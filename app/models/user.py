from peewee import BooleanField, IntegerField, TextField
from telegram import Bot, TelegramError

from app.core.database import BaseModel


class User(BaseModel):
    tg_user_id = IntegerField(primary_key=True)
    tg_login = TextField(unique=True)
    visible_name = TextField()
    locale = TextField()
    is_mute_enabled = BooleanField()

    class Meta:
        table_name = 'users'

    def send_personal_message(self, bot: Bot, *args, **kwargs):
        try:
            bot.send_message(self.tg_user_id, *args, **kwargs)
        except TelegramError:
            pass
