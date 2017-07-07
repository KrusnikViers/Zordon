from telegram.ext import CommandHandler
from .handlers.user import *


def set_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler(commands_map['start'], on_status))
    dispatcher.add_handler(CommandHandler(commands_map['status'], on_status))
    dispatcher.add_handler(CommandHandler(commands_map['activate'], on_activate))
    dispatcher.add_handler(CommandHandler(commands_map['deactivate'], on_deactivate))
