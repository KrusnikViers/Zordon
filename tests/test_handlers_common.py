from unittest.mock import MagicMock

from app.handlers.common import *
from .base_test import BaseTestCase


class TestCommonHandlers(BaseTestCase):
    def test_abort(self):
        self._mm_update.callback_query = MagicMock()
        self._mm_update.callback_query.message = MagicMock()
        self._mm_update.callback_query.message.chat_id = 123
        self._mm_update.callback_query.message.message_id = 456
        self._mm_bot.delete_message.return_value = True

        self.call_handler_with_mock(on_abort)

        self._mm_bot.delete_message.assert_called_once_with(
            chat_id=self._mm_update.callback_query.message.chat_id,
            message_id=self._mm_update.callback_query.message.message_id)

    def test_abort_too_old(self):
        self._mm_update.callback_query = MagicMock()
        self._mm_update.callback_query.message = MagicMock()
        self._mm_update.callback_query.message.chat_id = 123
        self._mm_update.callback_query.message.message_id = 456
        self._mm_bot.delete_message.return_value = False

        self.call_handler_with_mock(on_abort)

        self._mm_bot.delete_message.assert_called_once_with(
            chat_id=self._mm_update.callback_query.message.chat_id,
            message_id=self._mm_update.callback_query.message.message_id)
        self._mm_bot.callback_query.edit_message_text.assert_called_once_with(text=self.Any(), parse_mode='Markdown')
