from .common import *
from .activity import on_activity_add_with_name


@personal_command()
def message_handler(bot: Bot, update: Update, user: User):
    if user.pending_action == pending_user_actions['activity_add']:
        on_activity_add_with_name(bot, update, user)
