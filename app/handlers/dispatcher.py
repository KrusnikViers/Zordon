from telegram import Bot, Chat, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, TypeHandler, Updater
from telegram.ext.filters import Filters
import functools

from app.database.connection import DatabaseConnection
from app.core.configuration import Configuration
from app.handlers.chat_type import ChatType
from app.handlers.context import Context
from app.handlers.inline_menu import InlineMenu
from app.i18n.translations import Translations

from app.handlers.impl import basic, broadcasts, manage


class Dispatcher:
    def __init__(self, configuration: Configuration, updater: Updater, db_connection: DatabaseConnection,
                 translations: Translations):
        self.configuration = configuration
        self.db = db_connection
        self.translations = translations
        self.updater = updater
        self._bind_all(updater)

    def _handler(self, chat_filters: list, handler_function, bot: Bot, update: Update):
        if update.effective_user and update.effective_user.is_bot:
            return
        if not ChatType.is_valid(chat_filters, update):
            return

        try:
            with Context(update, bot, self.db, self.translations) as context:
                if context.group:
                    basic.process_group_changes(context)
                if handler_function:
                    handler_function(context)
        except Exception as exc:
            manage.on_handler_exception(self.updater.bot, self.configuration, self.db)
            raise exc

    def _make_handler(self, chat_filters: list, raw_callable):
        return functools.partial(Dispatcher._handler, self, chat_filters, raw_callable)

    def _bind_all(self, updater: Updater):
        handlers = [
            CommandHandler(['start', 'help'],
                           self._make_handler([ChatType.PRIVATE, ChatType.GROUP], basic.on_help_or_start)),
            CommandHandler(['clickme'],
                           self._make_handler([ChatType.GROUP], basic.on_click_here)),

            CommandHandler(['all'],
                           self._make_handler([ChatType.GROUP], broadcasts.on_all_request)),
            CommandHandler(['recall'],
                           self._make_handler([ChatType.GROUP], broadcasts.on_recall_request)),
            CallbackQueryHandler(self._make_handler([ChatType.CALLBACK_GROUP], broadcasts.on_recall_join),
                                 pattern=InlineMenu.pattern('recall_join', False)),
            CallbackQueryHandler(self._make_handler([ChatType.CALLBACK_GROUP], broadcasts.on_recall_decline),
                                 pattern=InlineMenu.pattern('recall_decline', False)),

            MessageHandler(Filters.all, self._make_handler([ChatType.GROUP], None)),
        ]

        for handler in handlers:
            updater.dispatcher.add_handler(handler)
