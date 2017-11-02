from telegram import Bot, TelegramError, Update

from app.core import commands
from app.models.user import User


def error_handler(bot: Bot, update: Update, error: TelegramError):
    send(bot, 'Telegram error reported:\n{0}\nUpdate:\n{1}'.format(str(error), update.to_json()))


def send(bot: Bot, text: str):
    superuser = User.maybe_get(rights=commands.superuser_rights_level)
    if superuser:
        superuser.send_message(bot, text=text)
