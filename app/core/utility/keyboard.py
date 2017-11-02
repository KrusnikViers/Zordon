from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from app.core import commands
from app.models.all import *


class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, markup: list, close_button_text):
        """" Markup expected to be list of rows, where each row is a list of tuples ('Button name', |Command|) """
        if close_button_text:
            markup.append([(close_button_text, commands.get('system_close_menu'))])
        super(InlineKeyboard, self).__init__(
            [[InlineKeyboardButton(text, callback_data=str(command.code)) for text, command in row] for row in markup])


class ChatKeyboard(ReplyKeyboardMarkup):
    _aliases = {
        'activity_menu': 'Activities menu',
        'activity_subscriptions': 'My activities',
        'system_cancel': 'Cancel',
        'user_menu': 'Profile',
    }

    def __init__(self, user: User):
        if user.pending_action != User.pending_actions['none']:
            markup = [['system_cancel']]
        elif user.mobile_layout:
            markup = [['activity_subscriptions'], ['activity_menu'], ['user_menu']]
        else:
            markup = [['activity_subscriptions', 'activity_menu', 'user_menu']]

        super(ChatKeyboard, self).__init__(
            [[KeyboardButton(self._aliases[command]) for command in row] for row in markup], resize_keyboard=True)
