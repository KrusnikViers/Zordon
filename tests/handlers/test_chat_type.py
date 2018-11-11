from unittest.mock import MagicMock, PropertyMock
from telegram import Chat

from tests.base import BaseTestCase
from app.handlers.chat_type import ChatType


class TestChatType(BaseTestCase):
    def test_is_valid(self):
        update = MagicMock()

        type(update).effective_chat = PropertyMock(return_value=None)
        self.assertFalse(
            ChatType.is_valid([ChatType.PRIVATE, ChatType.CALLBACK_PRIVATE, ChatType.GROUP, ChatType.CALLBACK_GROUP],
                              update))

        type(update).effective_chat = PropertyMock(return_value=MagicMock())
        type(update.effective_chat).type = Chat.PRIVATE
        self.assertTrue(ChatType.is_valid([ChatType.CALLBACK_PRIVATE], update))
        self.assertTrue(ChatType.is_valid([ChatType.CALLBACK_PRIVATE, ChatType.PRIVATE], update))

        type(update.effective_chat).type = Chat.GROUP
        self.assertTrue(ChatType.is_valid([ChatType.CALLBACK_GROUP], update))
        self.assertFalse(ChatType.is_valid([ChatType.CALLBACK_PRIVATE], update))

        type(update.effective_chat).type = Chat.SUPERGROUP
        self.assertTrue(ChatType.is_valid([ChatType.CALLBACK_GROUP], update))

        type(update).callback_query = PropertyMock(return_value=None)
        self.assertTrue(ChatType.is_valid([ChatType.GROUP], update))

        type(update.effective_chat).type = Chat.PRIVATE
        self.assertTrue(ChatType.is_valid([ChatType.PRIVATE], update))
