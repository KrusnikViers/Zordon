import functools

from telegram import Bot, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, Updater
from telegram.ext.filters import Filters

from app.database.connection import DatabaseConnection
from app.handlers.actions import Callback
from app.handlers.context import Context
from app.handlers.filters import Filter
from app.handlers.impl import basic, broadcasts, routing
from app.handlers.util.inline_menu import callback_pattern
from app.handlers.util.reports import ReportsSender
from app.i18n.translations import Translations


class Dispatcher:
    def __init__(self, updater: Updater, db_connection: DatabaseConnection,
                 translations: Translations):
        self.db = db_connection
        self.translations = translations
        self.updater = updater
        self._bind_all(updater)

    @staticmethod
    def _is_update_valid(filters: list, update: Update):
        return Filter.apply(filters, update) and \
               not (update.effective_user and update.effective_user.is_bot)

    def _handler(self, handler_function, input_filters: list, bot: Bot, update: Update):
        if not self._is_update_valid(input_filters, update):
            return

        try:
            with Context(update, bot, self.db, self.translations) as context:
                if context.group:
                    routing.update_group_memberships(context)
                handler_function(context)
        except Exception as exc:
            ReportsSender.report_exception(self.db)
            raise exc

    def _make_handler(self, raw_callable, input_filters: list = (Filter.FULL_DATA,)):
        return functools.partial(Dispatcher._handler, self, raw_callable, input_filters)

    def _bind_all(self, updater: Updater):
        handlers = [
            CommandHandler(['start', 'help'], self._make_handler(basic.on_help_or_start)),

            CommandHandler(['clickme'], self._make_handler(basic.on_click_here, [Filter.GROUP])),

            CommandHandler(['cancel'], self._make_handler(basic.on_reset_action)),
            CallbackQueryHandler(self._make_handler(broadcasts.on_recall_join, [Filter.CALLBACK]),
                                 pattern=callback_pattern(Callback.CANCEL, False)),

            CommandHandler(['report'], self._make_handler(basic.on_user_report_request)),

            CommandHandler(['all'], self._make_handler(broadcasts.on_all_request, [Filter.GROUP])),

            CommandHandler(['recall'],
                           self._make_handler(broadcasts.on_recall_request, [Filter.GROUP])),
            CallbackQueryHandler(self._make_handler(broadcasts.on_recall_join, [Filter.GROUP, Filter.CALLBACK]),
                                 pattern=callback_pattern(Callback.RECALL_JOIN, False)),
            CallbackQueryHandler(self._make_handler(broadcasts.on_recall_decline, [Filter.GROUP, Filter.CALLBACK]),
                                 pattern=callback_pattern(Callback.RECALL_DECLINE, False)),

            MessageHandler(Filters.all, self._make_handler(routing.dispatch_bare_message, [])),
        ]

        for handler in handlers:
            updater.dispatcher.add_handler(handler)
