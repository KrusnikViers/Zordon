from telegram import Bot, Update

from app.database.connection import DatabaseConnection
from app.i18n.translations import Translations
from app.handlers.scoped_context import ScopedContext


class Context(ScopedContext):
    def __init__(self, update: Update, bot: Bot, db: DatabaseConnection, translations: Translations):
        super(Context, self).__init__(update, bot, db, translations)

    def send_response_message(self, text, **kwargs):
        self.update.effective_chat.send_response_message(text, **kwargs)
