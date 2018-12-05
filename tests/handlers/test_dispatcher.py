from unittest.mock import MagicMock, PropertyMock
from telegram import Chat

from tests.base import BaseTestCase, InBotTestCase, MatcherAny
from app.database.scoped_session import ScopedSession
from app.handlers.dispatcher import Dispatcher
from app.handlers.input_filters import ChatFilter, InputFilters
from app.models.all import User


class TestDispatcher(BaseTestCase):
    def test_inner_handling(self):
        updater = MagicMock()
        instance = Dispatcher(MagicMock(), updater, MagicMock(), MagicMock())
        updater.dispatcher.add_handler.assert_called()

        handler_function = MagicMock()

        # Do not handle messages from other bots.
        update = MagicMock()
        type(update.effective_chat).type = Chat.GROUP
        type(update).callback_query = PropertyMock(return_value=None)
        type(update.effective_user).is_bot = PropertyMock(return_value=True)
        instance._handler(handler_function, InputFilters(), MagicMock(), update)
        self.assertFalse(handler_function.called)

        # Do not handle message of wrong type.
        type(update.effective_user).is_bot = PropertyMock(return_value=False)
        instance._handler(handler_function, InputFilters(chat=ChatFilter.PRIVATE), MagicMock(), update)
        self.assertFalse(handler_function.called)

        instance._handler(handler_function, InputFilters(chat=ChatFilter.GROUP), MagicMock(), update)
        handler_function.assert_called_once()


class TestDispatcherEx(InBotTestCase):
    def test_exception_caught(self):
        with ScopedSession(self.connection) as session:
            user = User(id=1234, login='test', name='Super User')
            session.add(user)

        configuration = MagicMock()
        type(configuration).superuser_login = PropertyMock(return_value='@test')
        bot = MagicMock()
        updater = MagicMock()
        type(updater).bot = PropertyMock(return_value=bot)

        instance = Dispatcher(configuration, updater, self.connection, MagicMock())
        updater.dispatcher.add_handler.assert_called()

        handler_function = MagicMock()
        handler_function.side_effect = Exception('something bad')

        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        type(update).callback_query = PropertyMock(return_value=None)
        type(update).effective_user = PropertyMock(return_value=None)
        type(update).message = PropertyMock(return_value=None)

        self.assertRaises(Exception, instance._handler, handler_function, InputFilters(), MagicMock(), update)
        handler_function.assert_called_once()
        bot.send_message.assert_called_once_with(1234, MatcherAny())
