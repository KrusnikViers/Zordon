import telegram as tg

from ..models import *
from .utils import personal_command

import app.handlers.activity as a
import app.handlers.participant as p
import app.handlers.superuser as su
import app.handlers.user as u


command_plain_aliases = {
    'Cancel action': u.on_cancel,
    'Do not disturb': u.on_deactivate,
    'Ready': u.on_activate,
    'Status': u.on_status,
    'Activities list': a.on_list,
    'Summon friends': p.on_summon,
    'Report bug': u.on_report,
    'Full information': su.on_full_information,
}


@personal_command()
def message_handler(bot: tg.Bot, update: tg.Update, user: User):
    message = update.message.text.strip()
    if message in command_plain_aliases:
        command_plain_aliases[message](bot, update, user)
    elif user.pending_action == pending_user_actions['a_new']:
        a.on_new_with_data(bot, update, user)
    elif user.pending_action == pending_user_actions['u_report']:
        u.on_report_with_data(bot, update, user)
