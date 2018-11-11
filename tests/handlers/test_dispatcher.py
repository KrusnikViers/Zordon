from unittest.mock import MagicMock, PropertyMock
from telegram import Chat

from tests.base import BaseTestCase
from app.handlers.dispatcher import Dispatcher
from app.handlers.chat_type import ChatType


class TestDispatcher(BaseTestCase):
    def test_inner_handling(self):
        updater = MagicMock()
        instance = Dispatcher(updater, MagicMock(), MagicMock())
        updater.dispatcher.add_handler.assert_called()

        handler_function = MagicMock()

        # Do not handle messages from other bots.
        update = MagicMock()
        type(update.effective_chat).type = Chat.GROUP
        type(update).callback_query = PropertyMock(return_value=None)
        type(update.effective_user).is_bot = PropertyMock(return_value=True)
        instance._handler([ChatType.GROUP], handler_function, MagicMock(), update)
        self.assertFalse(handler_function.called)

        # Do not handle message of wrong type.
        type(update.effective_user).is_bot = PropertyMock(return_value=False)
        instance._handler([ChatType.PRIVATE], handler_function, MagicMock(), update)
        self.assertFalse(handler_function.called)

        instance._handler([ChatType.GROUP], handler_function, MagicMock(), update)
        handler_function.assert_called_once()
