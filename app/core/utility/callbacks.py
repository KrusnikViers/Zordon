from telegram import Bot, TelegramError, Update

from app.core import commands
from app.models.user import User


def make_data(command, data: list) -> str:
    return ' '.join([commands.str_code(command)] + [str(x) for x in data])


def parse_data(update: Update) -> tuple:
    # First element is a command identifier
    return tuple(update.callback_query.data.split()[1:])


def make_handler_pattern(command, has_data: bool = False) -> str:
    return '^{0}{1}$'.format(commands.str_code(command), '\ .+' if has_data else '')


def maybe_update(bot: Bot, update: Update, user: User, text: str, reply_markup: object):
    if update.callback_query:
        try:
            update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
        except TelegramError:
            user.send_message(bot, text=text, reply_markup=reply_markup)
    else:
        user.send_message(bot, text=text, reply_markup=reply_markup)
