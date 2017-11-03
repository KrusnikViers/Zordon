from telegram import Bot, Update
from telegram.ext import CommandHandler

from app.common.i18n import translations
from app.core.utility import wrappers
from app.models.all import *


@wrappers.personal_command('user_menu')
def menu(bot: Bot, update: Update, user: User):
    rights_levels = [
        _('rl_desc_0'),
        _('rl_desc_1'),
        _('rl_desc_s'),
    ]
    notifications_status = _('enabled_p') if user.status == user.statuses['active'] else _('disabled_p')
    text = _('user_menu_text {login} {rights} {mode} {lang}').format(login=user.login,
                                                                     rights=rights_levels[user.rights],
                                                                     mode=notifications_status,
                                                                     lang=translations.get_full_name(user.locale))
    user.send_message(bot, text=text)


def get_handlers() -> list:
    return [
        CommandHandler('start', menu),
    ]
