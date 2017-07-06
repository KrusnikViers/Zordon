import telegram.ext
import telegram
from .models import *
from .utils import personal_command
from .definitions import superuser_login


cmd_start = "start"
cmd_status = "status"
cmd_activate = "ready"
cmd_deactivate = "do_not_disturb"


def _default_response(bot: telegram.Bot, update: telegram.Update, user: User):
    """ Reporting user status and providing common inline keyboard. Should be called only from handlers. """
    response = "{0}, currently you are {1}receiving notifications."\
        .format(update.effective_user.name, "" if user.is_active else "not ")
    if user.is_moderator:
        response += "\nYou have power to create new activities and appeal to your friends!"
    if update.effective_user.name == '@' + superuser_login:
        response += "\nYou are superuser. Use this power wisely."
    bot.send_message(chat_id=update.message.chat_id, text=response)


@personal_command
def _on_status(bot: telegram.Bot, update: telegram.Update, user: User):
    """ Default handler, that output basic information and inline keyboard. """
    _default_response(bot, update, user)


@personal_command
def _on_activate(bot: telegram.Bot, update: telegram.Update, user: User):
    """ Handler of user activation command """
    if not user.is_active:
        user.is_active = True
        user.save()
    _default_response(bot, update, user)


@personal_command
def _on_deactivate(bot: telegram.Bot, update: telegram.Update, user: User):
    """ Handler of user deactivation command """
    if user.is_active:
        user.is_active = False
        user.save()
    bot.send_message(chat_id=update.message.chat_id,
                     text="I will not disturb you now, friend.",
                     reply_markup=telegram.InlineKeyboardMarkup([[
                         telegram.InlineKeyboardButton('Ready again!', callback_data=cmd_activate)
                     ]]))


def set_handlers(dispatcher):
    dispatcher.add_handler(telegram.ext.CommandHandler(cmd_start, _on_status))
    dispatcher.add_handler(telegram.ext.CommandHandler(cmd_status, _on_status))
    dispatcher.add_handler(telegram.ext.CommandHandler(cmd_activate, _on_activate))
    dispatcher.add_handler(telegram.ext.CommandHandler(cmd_deactivate, _on_deactivate))
