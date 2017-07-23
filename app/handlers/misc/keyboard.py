from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from ...models import User
from ...definitions import pending_user_actions, command_text_aliases


class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, markup: list):
        super(InlineKeyboard, self).__init__(
            [[InlineKeyboardButton(text, callback_data=data) for text, data in row] for row in markup])


class ClosableInlineKeyboard(InlineKeyboard):
    def __init__(self, markup: list, cancel_text: str):
        super(ClosableInlineKeyboard, self).__init__(markup + [[(cancel_text, 'c_abort')]])


class ResponseInlineKeyboard(InlineKeyboard):
    def __init__(self, activity_name: str, is_accepted=None):
        markup = [[]]
        if not is_accepted:
            markup[0] += [('Join now', 'p_accept ' + activity_name), ('Coming', 'p_accept_later ' + activity_name)]
        if is_accepted or is_accepted is None:
            markup[0].append(('Decline', 'p_decline ' + activity_name))
        super(ResponseInlineKeyboard, self).__init__(markup)


class UserKeyboard(ReplyKeyboardMarkup):
    def __init__(self, user: User):
        markup = []
        if user.pending_action != pending_user_actions['none']:
            markup.append(['u_cancel'])
        markup.append(['u_deactivate' if user.is_active else 'u_activate', 'a_list'])
        if user.has_right_to('p_summon'):
            markup.append(['p_summon'])
        if user.has_right_to('su_full_information'):
            markup.append(['su_full_information'])

        command_to_text = {command: text for text, command in command_text_aliases.items()}
        super(UserKeyboard, self).__init__(
            [[KeyboardButton(command_to_text[command]) for command in row] for row in markup], resize_keyboard=True)
