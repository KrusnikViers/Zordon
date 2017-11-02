from telegram import Bot, Update

from app.core import commands
from app.models.all import *


def _get_user(bot: Bot, update: Update) -> User:
    user, is_created = User.get_or_create(telegram_id=update.effective_user.id,
                                          defaults={'login': update.effective_user.name})
    if is_created:
        superuser = User.maybe_get(rights_level=commands.superuser_rights_level)
        if superuser:
            superuser.send_message(bot, text='User {} joined!'.format(user.login))
    elif user.status == user.statuses['disabled_chat']:
        user.status = user.statuses['active']
        user.save()
        superuser = User.maybe_get(rights_level=commands.superuser_rights_level)
        if superuser:
            superuser.send_message(bot, text='User {} rejoined!'.format(user.login))
    if user.login != update.effective_user.name:
        user.telegram_login = update.effective_user.name
        user.save()
    return user


def personal_command(command: str):
    def personal_command_impl(decorated_handler):
        def decorated_handler_wrapper(bot: Bot, update: Update, user=None):
            # If command was received from callback query, mark it as received.
            if update.callback_query:
                update.callback_query.answer()

            if not user:
                user = _get_user(bot, update)

            if not user.able(command):
                user.send_message(text='Sorry, but you have not enough rights.')
            else:
                decorated_handler(bot, update, user)
        return decorated_handler_wrapper
    return personal_command_impl
