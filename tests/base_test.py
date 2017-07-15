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

    def set_callback_data(self, user_id, data):
        self._mm_update.effective_user = create_autospec(Update.effective_user)
        self._mm_update.effective_user.id = user_id
        self._mm_update.callback_query = create_autospec(CallbackQuery)
        self._mm_update.callback_query.data = data

    def set_message_text(self, text):
        self._mm_update.message = create_autospec(Message)
        self._mm_update.message.text = text
