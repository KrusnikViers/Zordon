from telegram import Update
from unittest import TestCase
from unittest.mock import patch, create_autospec, MagicMock

from app.handlers import common
from app.models import *

_on_activity_new_with_data_mock = patch('app.handlers.activity.on_new_with_data', autospec=True).start()
import app.handlers.messages as h_messages

_bot = create_autospec(Bot)
_update = MagicMock()


class TestMessagesHandlers(TestCase):
    def setUp(self):
        _on_activity_new_with_data_mock.reset_mock()
        _bot.reset_mock()
        _update.reset_mock()

        User.delete().execute()

    def test_message_routing_none(self):
        user = User.create(telegram_user_id=0)
        h_messages.message_handler(_bot, _update, user)
        self.assertFalse(_on_activity_new_with_data_mock.called)

    def test_message_routing_add_activity(self):
        user = User.create(telegram_user_id=0, pending_action=common.pending_user_actions['a_new'])
        _update.message.text = 'Sample name'
        h_messages.message_handler(_bot, _update, user)
        _on_activity_new_with_data_mock.assert_called_once_with(_bot, _update, user)
