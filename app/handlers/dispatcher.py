from telegram.ext import CommandHandler, Dispatcher

from app.handlers import simple


def set_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler('start', simple.on_start))
