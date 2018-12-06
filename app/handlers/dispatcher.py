from telegram import Bot, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, Updater
from telegram.ext.filters import Filters
import functools

from app.database.connection import DatabaseConnection
from app.core.configuration import Configuration
from app.handlers.input_filters import ChatFilter, MessageFilter, InputFilters, is_message_valid
from app.handlers.context import Context
from app.handlers.inline_menu import callback_pattern
from app.i18n.translations import Translations
from app.handlers import preprocessing

from app.handlers.impl import basic, broadcasts, manage


class Dispatcher:
    def __init__(self, configuration: Configuration, updater: Updater, db_connection: DatabaseConnection,
                 translations: Translations):
        self.configuration = configuration
        self.db = db_connection
        self.translations = translations
        self.updater = updater
        self._bind_all(updater)

    @staticmethod
    def _is_update_valid(filters: InputFilters, update: Update):
        return is_message_valid(filters, update) and \
               not (update.effective_user and update.effective_user.is_bot)

    def _handler(self, handler_function, input_filters, bot: Bot, update: Update):
        if not self._is_update_valid(input_filters, update):
            return

        try:
            with Context(update, bot, self.db, self.translations) as context:
                if context.group:
                    preprocessing.update_group_memberships(context)
                if handler_function:
                    handler_function(context)
        except Exception as exc:
            manage.on_handler_exception(self.updater.bot, self.configuration, self.db)
            raise exc

    def _make_handler(self, raw_callable, input_filters: InputFilters=InputFilters()):
        return functools.partial(Dispatcher._handler, self, raw_callable, input_filters)

    def _bind_all(self, updater: Updater):
        handlers = [
            CommandHandler(['start', 'help'], self._make_handler(basic.on_help_or_start)),
            CommandHandler(['clickme'], self._make_handler(basic.on_click_here, InputFilters(chat=ChatFilter.GROUP))),

            CommandHandler(['all'], self._make_handler(broadcasts.on_all_request, InputFilters(chat=ChatFilter.GROUP))),
            CommandHandler(['recall'],
                           self._make_handler(broadcasts.on_recall_request, InputFilters(chat=ChatFilter.GROUP))),
            CallbackQueryHandler(self._make_handler(broadcasts.on_recall_join,
                                                    InputFilters(chat=ChatFilter.GROUP,
                                                                 message=MessageFilter.CALLBACK)),
                                 pattern=callback_pattern('recall_join', False)),
            CallbackQueryHandler(self._make_handler(broadcasts.on_recall_decline,
                                                    InputFilters(chat=ChatFilter.GROUP,
                                                                 message=MessageFilter.CALLBACK)),
                                 pattern=callback_pattern('recall_decline', False)),

            MessageHandler(Filters.all, self._make_handler(None, InputFilters(chat=ChatFilter.GROUP))),
        ]

        for handler in handlers:
            updater.dispatcher.add_handler(handler)
