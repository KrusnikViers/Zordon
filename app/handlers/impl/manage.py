import traceback

from telegram import Bot

from app.core.configuration import Configuration
from app.database.connection import DatabaseConnection
from app.database.scoped_session import ScopedSession
from app.models.all import User


def _send_message_to_superuser(bot: Bot, configuration: Configuration, session, message: str):
    if configuration.superuser_login:
        superuser = session.query(User).filter_by(login=configuration.superuser_login[1:]).one_or_none()
        if superuser:
            bot.send_message(superuser.id, message)


def on_handler_exception(bot: Bot, configuration: Configuration, connection: DatabaseConnection):
    with ScopedSession(connection) as session:
        _send_message_to_superuser(bot, configuration, session, traceback.format_exc())
