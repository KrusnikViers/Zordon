import telegram as tg

from ..models import *
from .utils import personal_command

import app.handlers.activity as a
import app.handlers.participant as p
import app.handlers.superuser as su
import app.handlers.user as u


@personal_command()
def message_handler(bot: tg.Bot, update: tg.Update, user: User):
    command_handlers = {
        'u_cancel': u.on_cancel,
        'u_deactivate': u.on_deactivate,
        'u_activate': u.on_activate,
        'u_status': u.on_status,
        'a_list': a.on_list,
        'p_summon': p.on_summon,
        'u_report': u.on_report,
        'su_full_information': su.on_full_information,
    }

    message = update.message.text.strip()
    if message in command_text_aliases:
        command = command_text_aliases[message]
        command_handlers[command](bot, update, user)
    elif user.pending_action == pending_user_actions['a_new']:
        a.on_new_with_data(bot, update, user)
    elif user.pending_action == pending_user_actions['u_report']:
        u.on_report_with_data(bot, update, user)
