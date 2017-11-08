from telegram import Bot, TelegramError, Update
from telegram.ext import CallbackQueryHandler

from app.core.utility import callbacks, wrappers
from app.models.all import *


@wrappers.personal_command('system_close_menu')
def close(bot: Bot, update: Update, user: User):
    if update.callback_query:
        message = update.callback_query.message
        try:
            if not bot.delete_message(message.chat.id, message.message_id):
                # If we have failed in deleting the message, try to at least remove the inline menu.
                update.callback_query.edit_message_reply_markup(reply_markup=None)
        except TelegramError:
            # This is fine(c). This exception simply means, that message is too old to be modified.
            pass


def get_handlers() -> list:
    return [
        CallbackQueryHandler(close, pattern=callbacks.make_handler_pattern('system_close_menu')),
    ]
