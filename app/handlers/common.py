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
        if not update.effective_user:
            return
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
    keymap = [[
        KeyboardButton('/' + (commands_map['deactivate'] if user.is_active else commands_map['activate'])),
        KeyboardButton('/' + commands_map['status'])
    ]]
    if user.has_right('summon'):
        keymap[0].append(KeyboardButton('/' + commands_map['summon']))
    keymap[0].append(KeyboardButton('/' + commands_map['activity_list']))
    return ReplyKeyboardMarkup(keymap, resize_keyboard=True)
