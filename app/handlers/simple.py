from telegram import Bot, Update

from app.handlers.base import translatable_handler


@translatable_handler
def on_start(bot: Bot, update: Update):
    update.effective_chat.send_message(text=_('start_message'))
