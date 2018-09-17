from telegram import Bot, Chat, Update
from telegram.ext import CommandHandler, Updater
import functools

from app.database.connection import DatabaseConnection
from app.i18n.translations import Translations
from app.handlers.context import Context

from app.handlers.impl import common, user


class Dispatcher:
    def __init__(self, updater: Updater, db_connection: DatabaseConnection, translations: Translations):
        self.db = db_connection
        self.translations = translations
        self._bind_all(updater)

    def _handler(self, handler_function, bot: Bot, update: Update):
        if update.effective_chat and update.effective_chat.type in [Chat.PRIVATE, Chat.GROUP, Chat.SUPERGROUP]:
            with Context(update, bot, self.db, self.translations) as context:
                common.maybe_greet_user(context)
                handler_function(context)

    def _make_handler(self, raw_callable):
        return functools.partial(Dispatcher._handler, self, raw_callable)

    def _bind_all(self, updater: Updater):
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler(['start', 'help'], self._make_handler(common.on_help_or_start)))
        dispatcher.add_handler(CommandHandler(['setup', 'menu'], self._make_handler(user.on_menu_request)))
