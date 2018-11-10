from telegram import Bot, Chat, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, Updater
from telegram.ext.filters import Filters
import functools

from app.database.connection import DatabaseConnection
from app.handlers.chat_type import ChatType
from app.handlers.context import Context
from app.handlers.inline_menu import InlineMenu
from app.i18n.translations import Translations

from app.handlers.impl import basic, massive_mentions


class Dispatcher:
    def __init__(self, updater: Updater, db_connection: DatabaseConnection, translations: Translations):
        self.db = db_connection
        self.translations = translations
        self._bind_all(updater)

    def _handler(self, chat_filters: list, handler_function, bot: Bot, update: Update):
        if update.effective_user and update.effective_user.is_bot:
            return
        if not ChatType.is_valid(chat_filters, update):
            return
        with Context(update, bot, self.db, self.translations) as context:
            if context.group:
                basic.process_group_changes(context)
            if handler_function:
                handler_function(context)

    def _make_handler(self, chat_filters: list, raw_callable):
        return functools.partial(Dispatcher._handler, self, chat_filters, raw_callable)

    def _bind_all(self, updater: Updater):
        handlers = [
            CommandHandler(['start', 'help'],
                           self._make_handler([ChatType.PRIVATE, ChatType.GROUP], basic.on_help_or_start)),

            CommandHandler(['all'],
                           self._make_handler([ChatType.GROUP], massive_mentions.on_all_request)),
            CommandHandler(['call'],
                           self._make_handler([ChatType.GROUP], massive_mentions.on_call_request)),
            CallbackQueryHandler(self._make_handler([ChatType.CALLBACK_GROUP], massive_mentions.on_call_join),
                                 pattern=InlineMenu.pattern('call_join', True)),
            CallbackQueryHandler(self._make_handler([ChatType.CALLBACK_GROUP], massive_mentions.on_call_decline),
                                 pattern=InlineMenu.pattern('call_decline', True)),

            MessageHandler(Filters.status_update.new_chat_members, self._make_handler([ChatType.GROUP], None)),
            MessageHandler(Filters.status_update.left_chat_member, self._make_handler([ChatType.GROUP], None)),
        ]

        for handler in handlers:
            updater.dispatcher.add_handler(handler)
