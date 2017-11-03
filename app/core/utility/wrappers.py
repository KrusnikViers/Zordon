from telegram import Bot, Update

from app.common import credentials, database
from app.common.i18n import translations
from app.core import commands
from app.core.utility import report
from app.models.all import *


def _get_and_validate_user(bot: Bot, update: Update) -> User:
    user, is_created = User.get_or_create(telegram_id=update.effective_user.id,
                                          defaults={'login': update.effective_user.name})
    # Validate all user information
    if is_created:
        user.rights = commands.superuser_rights_level if user.login == credentials.superuser else 0
        report.send(bot, 'I: {0} joined; rights: {1}'.format(user.login, user.rights))
        user.save()

    if user.login != update.effective_user.name:
        report.send(bot, 'I: {0} -> {1}'.format(user.login, update.effective_user.name))
        user.login = update.effective_user.name
        user.save()

    if user.status == user.statuses['disabled_chat']:
        report.send(bot, 'I: {} rejoined'.format(user.login))
        user.status = user.statuses['active']
        user.save()

    return user


def personal_command(command: str):
    def personal_command_impl(decorated_handler):
        @database.database.atomic()
        def decorated_handler_wrapper(bot: Bot, update: Update, user=None):
            # If command was received from callback query, mark it as received.
            if update.callback_query:
                update.callback_query.answer()

            # Get user, if it was not fetched earlier.
            if not user:
                user = _get_and_validate_user(bot, update)

            # Check user rights, and, if everything is ok, call handler itself.
            translations.get(update, user).install()
            if not user.able(command):
                user.send_message(bot, text=_('rl_forbidden'))
            else:
                decorated_handler(bot, update, user)
        return decorated_handler_wrapper
    return personal_command_impl
