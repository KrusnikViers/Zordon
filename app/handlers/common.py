from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
from ..models import User


commands_map = {
    # User-related commands
    'start': 'start',
    'status': 'status',
    'activate': 'ready',
    'deactivate': 'do_not_disturb',

    # Commands with activities
    'activity_list': 'activities_list',
    'activity_add': 'add_activity',  # (moderator-only)
    'activity_rem': 'remove_activity',  # (superuser-only)
    'subscribe': 'subscribe',
    'unsubscribe': 'unsubscribe',

    # Summoning commands
    'summon': 'summon',  # (moderator-only)
    'join': 'will_join',
    'later': 'will_join_later',
    'decline': 'will_not_join',

    # Moderating the moderators (superuser-only)
    'moderator_list': 'list_moderators',
    'moderator_add': 'add_moderator',
    'moderator_remove': 'remove_moderator'
}


def personal_command(decorated_handler):
    def wrapper(bot: Bot, update: Update):
        user = User.get_or_create(telegram_id=update.effective_user.id,
                                  defaults={'is_active': True,
                                            'is_moderator': False,
                                            'telegram_login': update.effective_user.name})[0]
        if user.telegram_login != update.effective_user.name:
            user.telegram_login = update.effective_user.name
            user.save()
        decorated_handler(bot, update, user)
    return wrapper


def keyboard_for_user(user: User):
    activation_command = 'deactivate' if user.is_active else 'activate'
    possible_commands = [activation_command, 'status', 'summon', 'activity_list', 'moderator_list']
    keyboard_row = [KeyboardButton('/' + commands_map[x]) for x in possible_commands if user.has_right(x)]
    return ReplyKeyboardMarkup([keyboard_row], resize_keyboard=True)
