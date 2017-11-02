from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackQueryHandler

from app.core.utility import wrappers, callbacks
from app.models.all import *


@wrappers.personal_command('user_menu')
def menu(bot: Bot, update: Update, user: User):
    rights_level_name = [
        'Basic',
        'Advanced',
        'Superuser',
    ]
    header = 'Greetings, {}!\n\n'.format(user.login)
    header += 'Rights level: {}\n'.format(rights_level_name[user.rights])
    header += 'Notifications: {}\n'.format('Enabled' if user.status == User.statuses['active'] else 'Disabled')
    user.send_message(bot, text=header)


def get_handlers() -> list:
    return [
        CommandHandler('start', menu),
        CallbackQueryHandler(menu, callbacks.make_pattern('user_menu')),
    ]
