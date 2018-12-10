from unittest.mock import MagicMock, PropertyMock

from telegram import Chat

from app.handlers.input_filters import ChatFilter, InputFilters, MessageFilter, is_message_valid
from tests.base import BaseTestCase


class TestInputFilters(BaseTestCase):
    def test_is_valid(self):
        update = MagicMock()

        type(update).effective_chat = PropertyMock(return_value=None)
        self.assertFalse(is_message_valid(InputFilters(), update))

        type(update).effective_chat = PropertyMock(return_value=MagicMock())
        type(update.effective_chat).type = Chat.CHANNEL
        self.assertFalse(is_message_valid(InputFilters(), update))

        type(update.effective_chat).type = Chat.PRIVATE
        self.assertTrue(is_message_valid(InputFilters(chat=ChatFilter.PRIVATE), update))
        self.assertTrue(is_message_valid(InputFilters(chat=ChatFilter.PRIVATE, message=MessageFilter.CALLBACK), update))

        type(update.effective_chat).type = Chat.GROUP
        self.assertTrue(is_message_valid(InputFilters(chat=ChatFilter.GROUP, message=MessageFilter.CALLBACK), update))

        type(update.effective_chat).type = Chat.SUPERGROUP
        self.assertTrue(is_message_valid(InputFilters(chat=ChatFilter.GROUP), update))
