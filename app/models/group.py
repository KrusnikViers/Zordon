from peewee import CompositeKey, IntegerField, TextField, ForeignKeyField
from telegram import Bot, TelegramError

from app.core.database import BaseModel
from app.models.user import User


class Group(BaseModel):
    tg_chat_id = IntegerField(primary_key=True)
    name = TextField()
    locale = TextField()

    class Meta:
        table_name = 'groups'

    def send_message(self, bot: Bot, *args, **kwargs):
        try:
            bot.send_message(self.tg_chat_id, *args, **kwargs)
        except TelegramError:
            pass


class GroupMember(BaseModel):
    user = ForeignKeyField(User)
    group = ForeignKeyField(Group)

    class Meta:
        table_name = 'group_members'
        primary_key = CompositeKey('user', 'group')
