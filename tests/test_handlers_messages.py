from telegram import Update
from unittest import TestCase
from unittest.mock import patch, create_autospec

from app.handlers import common
from app.models import *

_on_activity_add_with_name_mock = patch('app.handlers.activity.on_activity_add_with_name', autospec=True).start()
import app.handlers.messages as h_messages

_bot = create_autospec(Bot)
_update = Update(0)


class TestMessagesHandlers(TestCase):
    def setUp(self):
        _on_activity_add_with_name_mock.reset_mock()

        User.delete().execute()

    def test_message_routing_none(self):
        user = User.create(telegram_user_id=0)
        h_messages.message_handler(_bot, _update, user)
        self.assertFalse(_on_activity_add_with_name_mock.called)

    def test_message_routing_add_activity(self):
        user = User.create(telegram_user_id=0, pending_action=common.pending_user_actions['activity_add'])
        h_messages.message_handler(_bot, _update, user)
        _on_activity_add_with_name_mock.assert_called_once_with(_bot, _update, user)
