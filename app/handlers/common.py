from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
from ..models import User


commands_map = {
    # User-related commands
    'start': 'start',
    'status': 'status',
    'activate': 'ready',
    'deactivate': 'do_not_disturb',

    # Commands with activities
    'activity_list': 'list_activities',
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


def personal_command(command):
    def personal_command_impl(decorated_handler):
        def wrapper(bot: Bot, update: Update):
            user = User.get_or_create(telegram_user_id=update.effective_user.id,
                                      defaults={'telegram_login': update.effective_user.name,
                                                'telegram_chat_id': update.message.chat_id})[0]
            user.validate_info(update.effective_user.name)
            if command and not user.has_right(command):
                user.send_message(bot,
                                  text='Unfortunately, you have not enough rights to execute this command.',
                                  reply_markup=keyboard_for_user(user))
            else:
                decorated_handler(bot, update, user)
        return wrapper
    return personal_command_impl


def keyboard_for_user(user: User):
    activation_command = 'deactivate' if user.is_active else 'activate'
    possible_commands = [activation_command, 'status', 'summon', 'activity_list', 'moderator_list']
    keyboard_row = [KeyboardButton('/' + commands_map[x]) for x in possible_commands if user.has_right(x)]
    return ReplyKeyboardMarkup([keyboard_row], resize_keyboard=True)
