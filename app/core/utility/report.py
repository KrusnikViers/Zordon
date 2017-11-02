from telegram import Bot, TelegramError, Update

from app.core import commands
from app.models.user import User


def error_handler(bot: Bot, update: Update, error: TelegramError):
    text = 'I: Error: ' + str(error) + ', update:\n' + str(update)
    send(bot, text)


def send(bot: Bot, text: str):
    superuser = User.maybe_get(rights=commands.superuser_rights_level)
    if superuser:
        superuser.send_message(bot, text=text)
