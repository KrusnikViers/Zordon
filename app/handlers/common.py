from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from ..models import User


commands_map = {
    # User-related commands
    'start': 'start',
    'status': 'status',
    'activate': 'ready',
    'deactivate': 'do_not_disturb',
    'cancel': 'cancel',

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
    'moderator_remove': 'remove_moderator',
}


pending_user_actions = {
    'none': 0,
    'activity_add': 1,
}


def build_inline_keyboard(buttons: list):
    if not buttons:
        return None
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(button[0], callback_data=button[1]) for button in row] for row in buttons])


def build_default_keyboard(user: User):
    activation_command = 'deactivate' if user.is_active else 'activate'
    buttons = [[activation_command, 'status', 'summon'], ['activity_list', 'moderator_list']]
    markup = [[KeyboardButton('/' + commands_map[x]) for x in row if user.has_right(x)] for row in buttons]
    return ReplyKeyboardMarkup(markup, resize_keyboard=True)


def callback_only(decorated_handler):
    def handler_wrapper(bot: Bot, update: Update):
        if update.callback_query:
            return decorated_handler(bot, update)
    return handler_wrapper


def send_response(user: User, bot: Bot, response):
    if not response:
        return
    if isinstance(response, tuple):
        user.send_message(bot, text=response[0], reply_markup=response[1])
    else:
        user.send_message(bot, text=response)


def personal_command(command=None):
    def personal_command_impl(decorated_handler):
        def decorated_handler_wrapper(bot: Bot, update: Update, user=None):
            if update.callback_query:
                update.callback_query.answer()

            if not user:
                user = User.get_or_create(telegram_user_id=update.effective_user.id,
                                          defaults={'telegram_login': update.effective_user.name})[0]
                if user.is_disabled_chat or user.telegram_login != update.effective_user.name:
                    user.telegram_login = update.effective_user.name
                    user.is_disabled_chat = False
                    user.save()

            if command and not user.has_right(command):
                send_response(user, bot, ('Not enough rights', build_default_keyboard(user)))
            else:
                send_response(user, bot, decorated_handler(bot, update, user))
        return decorated_handler_wrapper
    return personal_command_impl
