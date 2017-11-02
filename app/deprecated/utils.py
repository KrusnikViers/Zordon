from app.core.misc.keyboard import *
from telegram import Update, Bot

from app.deprecated.definitions import commands_set


class CallbackUtil:
    @staticmethod
    def edit(update: Update, text: str, reply_markup=None):
        if not update.callback_query:
            return

        if text:
            update.callback_query.edit_message_text(text=text)
        if reply_markup:
            update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)

    @staticmethod
    def update_selection(bot: Bot, update: Update, new_data):
        if isinstance(new_data, tuple):
            CallbackUtil.edit(update, *new_data)
        else:
            CallbackUtil.remove_message(bot, update)

    @staticmethod
    def get_data(callback_data: str)->str:
        return callback_data.split(' ', 1)[1]

    @staticmethod
    def remove_message(bot: Bot, update: Update):
        if not bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id):
            CallbackUtil.edit(update, 'Message is not valid any more')


def callback_only(decorated_handler):
    def handler_wrapper(bot: Bot, update: Update):
        if update.callback_query:
            return decorated_handler(bot, update)
    return handler_wrapper


def _send_response(user: User, bot: Bot, response):
    if not response:
        return
    if isinstance(response, tuple):
        user.send_message(bot, text=response[0], reply_markup=response[1])
    else:
        user.send_message(bot, text=response)


def personal_command(command=None):
    if command:
        assert command in commands_set

    def personal_command_impl(decorated_handler):
        def decorated_handler_wrapper(bot: Bot, update: Update, user=None):
            if update.callback_query:
                update.callback_query.answer()

            if not user:
                user, is_created = User.get_or_create(telegram_user_id=update.effective_user.id,
                                                      defaults={'telegram_login': update.effective_user.name})
                if user.is_disabled_chat or user.telegram_login != update.effective_user.name:
                    user.telegram_login = update.effective_user.name
                    user.is_disabled_chat = False
                    user.save()
                if is_created:
                    User.send_message_to_superuser(bot, text='{0} joined'.format(user.telegram_login))

            if command and not user.has_right_to(command):
                _send_response(user, bot, ('Not enough rights', UserKeyboard(user)))
            else:
                _send_response(user, bot, decorated_handler(bot, update, user))
        return decorated_handler_wrapper
    return personal_command_impl
