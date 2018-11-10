from telegram import Bot, Chat, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, Updater
from telegram.ext.filters import Filters
import functools

from app.database.connection import DatabaseConnection
from app.handlers.callback_utils import handler_pattern
from app.handlers.context import Context
from app.i18n.translations import Translations

from app.handlers.impl import basic, massive_mentions


class Dispatcher:
    def __init__(self, updater: Updater, db_connection: DatabaseConnection, translations: Translations):
        self.db = db_connection
        self.translations = translations
        self._bind_all(updater)

    @staticmethod
    def _should_process(update: Update) -> bool:
        if not update.effective_chat or update.effective_chat.type not in [Chat.PRIVATE, Chat.GROUP, Chat.SUPERGROUP]:
            return False
        if update.effective_user and update.effective_user.is_bot:
            return False
        return True

    def _handler(self, handler_function, bot: Bot, update: Update):
        if not Dispatcher._should_process(update):
            return
        with Context(update, bot, self.db, self.translations) as context:
            basic.process_users_and_groups(context)
            # Empty functions are allowed for informational messages, that should be processed by context only.
            if handler_function:
                handler_function(context)

    def _make_handler(self, raw_callable):
        return functools.partial(Dispatcher._handler, self, raw_callable)

    def _bind_all(self, updater: Updater):
        handlers = [
            CommandHandler(['start', 'help'], self._make_handler(basic.on_help_or_start)),

            CommandHandler(['all'], self._make_handler(massive_mentions.on_all_request)),
            CommandHandler(['call'], self._make_handler(massive_mentions.on_call_request)),
            CallbackQueryHandler(self._make_handler(massive_mentions.on_call_join),
                                 pattern=handler_pattern('call_join', True)),
            CallbackQueryHandler(self._make_handler(massive_mentions.on_call_decline),
                                 pattern=handler_pattern('call_decline', True)),

            MessageHandler(Filters.status_update.new_chat_members, None),
            MessageHandler(Filters.status_update.left_chat_member, None),
            MessageHandler(Filters.status_update.new_chat_title, None),
        ]

        for handler in handlers:
            updater.dispatcher.add_handler(handler)
