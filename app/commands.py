from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from .handlers.activity import *
from .handlers.messages import *
from .handlers.user import *


def set_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler(commands_map['start'], on_status))
    dispatcher.add_handler(CommandHandler(commands_map['status'], on_status))
    dispatcher.add_handler(CommandHandler(commands_map['activate'], on_activate))
    dispatcher.add_handler(CommandHandler(commands_map['deactivate'], on_deactivate))
    dispatcher.add_handler(CallbackQueryHandler(on_cancel, pattern="^cancel$"))

    dispatcher.add_handler(CommandHandler(commands_map['activity_list'], on_activity_list))
    dispatcher.add_handler(CommandHandler(commands_map['activity_add'], on_activity_add))
    dispatcher.add_handler(CallbackQueryHandler(on_activity_add, pattern="^activity_add$"))
    dispatcher.add_handler(CommandHandler(commands_map['activity_rem'], on_activity_rem))
    dispatcher.add_handler(CallbackQueryHandler(on_activity_rem, pattern="^activity_rem$"))
    dispatcher.add_handler(CallbackQueryHandler(on_activity_rem_with_name, pattern="^activity_rem.+$"))

    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
