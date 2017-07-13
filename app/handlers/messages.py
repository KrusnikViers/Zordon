from .activity import on_activity_add_with_name, on_activity_list
from .common import *
from .management import on_raw_data
from .summon import on_summon
from .user import on_cancel, on_activate, on_deactivate, on_status


command_plain_aliases = {
    'Cancel action': on_cancel,
    'Do not disturb': on_deactivate,
    'Ready': on_activate,
    'Status': on_status,
    'Activities list': on_activity_list,
    'Summon friends': on_summon,
    'Raw data': on_raw_data,
}


@personal_command()
def message_handler(bot: Bot, update: Update, user: User):
    message = update.message.text.strip()
    if message in command_plain_aliases:
        command_plain_aliases[message](bot, update, user)
    if user.pending_action == pending_user_actions['activity_add']:
        on_activity_add_with_name(bot, update, user)
