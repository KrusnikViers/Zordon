from telegram import Update, CallbackQuery, Message
from unittest import TestCase
from unittest.mock import MagicMock, create_autospec

from app.models import *


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()

        Subscription.delete().execute()
        Participant.delete().execute()
        User.delete().execute()
        Activity.delete().execute()

        self._mm_bot = MagicMock()
        self._mm_update = MagicMock
        self._mm_update.callback_query = None
        self._mm_update.message = None

    class Any:
        def __eq__(self, other):
            return True

    class KeyboardMatcher:
        def __init__(self, expectations):
            self.expectations = expectations

        def __eq__(self, other):
            if len(self.expectations) != len(other.inline_keyboard):
                return False
            for i in range(0, len(self.expectations)):
                if other.inline_keyboard[i][0].callback_data != self.expectations[i]:
                    return False
            return True

    def call_handler_with_mock(self, handler, user: object):
        if user:
            handler(self._mm_bot, self._mm_update, user)
        else:
            handler(self._mm_bot, self._mm_update)

    def set_callback_data(self, user: User, data):
        self._mm_update.effective_user = create_autospec(Update.effective_user)
        self._mm_update.effective_user.id = user.telegram_user_id
        self._mm_update.effective_user.name = user.telegram_login
        self._mm_update.callback_query = create_autospec(CallbackQuery)
        self._mm_update.callback_query.data = data

    def set_message_text(self, text):
        self._mm_update.message = create_autospec(Message)
        self._mm_update.message.text = text
