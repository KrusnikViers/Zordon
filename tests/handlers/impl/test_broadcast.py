from unittest.mock import MagicMock, PropertyMock
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tests.base import InBotTestCase, ScopedSession
from app.models.all import *
from app.handlers.impl import broadcasts


class TestBasicHandlers(InBotTestCase):
    class MatcherResponseKeyboard:
        def __eq__(self, keyboard):
            return keyboard.inline_keyboard == [[InlineKeyboardButton('recall_join', callback_data='1'),
                                                 InlineKeyboardButton('recall_decline', callback_data='2')]]

    @staticmethod
    def _create_context(session) -> MagicMock:
        group = Group(id=1000, name='group')
        sender = User(id=1001, name='sender')
        sender.groups.append(group)
        session.add(group)
        session.add(sender)

        context = MagicMock()
        type(context).group = PropertyMock(return_value=group)
        type(context).sender = PropertyMock(return_value=sender)
        type(context.update.effective_chat).id = PropertyMock(return_value=1002)
        context.command_arguments.return_value = ''

        return context

    @staticmethod
    def _reset_message(context):
        message = MagicMock()
        type(message).message_id = PropertyMock(return_value=1003)
        context.send_response_message.reset_mock()
        context.send_response_message.return_value = message

    def test_empty_broadcasts(self):
        with ScopedSession(self.connection) as session:
            context = self._create_context(session)
            invited = User(id=1, name='invited')
            invited.groups.append(context.group)
            session.add(invited)
            self._reset_message(context)
            broadcasts.on_all_request(context)
            context.send_response_message.assert_called_once_with('all_from_sender\n\ninvited')
            self._reset_message(context)
            broadcasts.on_recall_request(context)
            context.send_response_message.assert_called_once_with('recall_from_sender\n\nrecall_not_answered_invited',
                                                                  reply_markup=self.MatcherResponseKeyboard())


    def test_messaged_broadcasts(self):
        with ScopedSession(self.connection) as session:
            context = self._create_context(session)
            context.command_arguments.return_value = 'some_message'
            invited = User(id=1, name='invited')
            invited.groups.append(context.group)
            session.add(invited)
            self._reset_message(context)
            broadcasts.on_all_request(context)
            context.send_response_message.assert_called_once_with('some_message\nall_with_text_from_sender\n\ninvited')
            self._reset_message(context)
            broadcasts.on_recall_request(context)
            context.send_response_message.assert_called_once_with(
                'some_message\nrecall_with_text_from_sender\n\nrecall_not_answered_invited',
                reply_markup=self.MatcherResponseKeyboard())

    def test_no_users_broadcast(self):
        with ScopedSession(self.connection) as session:
            context = self._create_context(session)
            broadcasts.on_all_request(context)
            context.send_response_message.assert_called_once_with('no_users_for_broadcast_message')
            context.send_response_message.reset_mock()
            broadcasts.on_recall_request(context)
            context.send_response_message.assert_called_once_with('no_users_for_broadcast_message')
            context.send_response_message.reset_mock()
