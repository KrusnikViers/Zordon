from telegram.ext import CommandHandler, Dispatcher
from telegram import Bot, Update

from app.handlers.base import translatable_handler


def set_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler('start', _on_start))


@translatable_handler
def _on_start(bot: Bot, update: Update):
    update.effective_chat.send_message(text=_('start_message'))
