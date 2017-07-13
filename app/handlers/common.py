from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from ..models import User
from ..definitions import commands_set, pending_user_actions


def build_inline_keyboard(buttons: list):
    if not buttons:
        return None
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(button[0], callback_data=button[1]) for button in row] for row in buttons])


def build_default_keyboard(user: User):
    buttons = [['Do not disturb' if user.is_active else 'Ready', 'Status'], ['Activities list']]
    if user.pending_action != pending_user_actions['none']:
        buttons[0].insert(0, 'Cancel action')
    if user.has_right('p_summon'):
        buttons[1].append('Summon friends')
    if user.has_right('su_full_information'):
        buttons[1].append('Full information')
    return ReplyKeyboardMarkup([[KeyboardButton(x) for x in row] for row in buttons], resize_keyboard=True)


def build_summon_response_keyboard(activity_name: str):
    return build_inline_keyboard([[('Join now', 'p_accept_now ' + activity_name),
                                   ('Coming', 'p_accept_later ' + activity_name),
                                   ('Decline', 'p_decline ' + activity_name)]])


def get_info_from_callback_data(callback_data: str)->str:
    return callback_data.split(' ', 1)[1]


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
    if command:
        assert command in commands_set

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
