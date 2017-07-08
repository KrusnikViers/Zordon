import telegram
from .common import *
from ..models import *
from ..definitions import superuser_login


@personal_command
def on_status(bot: telegram.Bot, update: telegram.Update, user: User):
    response = "Your current status: "
    response += "Ready (receiving all notifications)." if user.is_active else "DnD (do not want to be disturbed)."
    if update.effective_user.name == '@' + superuser_login:
        response += "\nYou have superuser rights. Use this power wisely."
    elif user.is_moderator:
        response += "\nAlso, you have rights to create activities or summon other people."
    user.send_message(bot, text=response, reply_markup=keyboard_for_user(user))


@personal_command
def on_activate(bot: telegram.Bot, update: telegram.Update, user: User):
    if user.is_active:
        user.send_message(bot, text="You were already receiving all notifications.")
    else:
        user.is_active = True
        user.save()
        user.send_message(bot,
                          text="Now you are receiving all notifications again.",
                          reply_markup=keyboard_for_user(user))
        # TODO: send all pending summons


@personal_command
def on_deactivate(bot: telegram.Bot, update: telegram.Update, user: User):
    if not user.is_active:
        user.send_message(bot, text="Summon notifications were already suppressed.")
    else:
        user.is_active = False
        user.save()
        user.send_message(bot,
                          text="Now you would not be disturbed with summon notifications.",
                          reply_markup=keyboard_for_user(user))
