from unittest.mock import MagicMock, PropertyMock

from telegram import InlineKeyboardButton, TelegramError

from app.handlers.impl import broadcasts
from app.models.all import *
from tests.base import InBotTestCase, ScopedSession


class TestBroadcastHandlers(InBotTestCase):
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
        type(context).session = PropertyMock(return_value=session)
        type(context.update.effective_chat).id = PropertyMock(return_value=1002)
        context.command_arguments.return_value = ''

        return context

    @staticmethod
    def _reset_message(context):
        message = MagicMock()
        type(message).message_id = PropertyMock(return_value=1003)
        context.send_response_message.reset_mock()
        context.send_response_message.return_value = message
        context.update.callback_query.edit_message_text.reset_mock()

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

    def test_recall_accept_decline(self):
        with ScopedSession(self.connection) as session:
            context = self._create_context(session)
            other_users = [User(id=i, name='user ' + str(i)) for i in range(1, 4)]
            for user in other_users:
                context.group.users.append(user)
                session.add(user)

            # Initial call.
            self._reset_message(context)
            broadcasts.on_recall_request(context)
            context.send_response_message.assert_called_once_with(
                'recall_from_sender\n\nrecall_not_answered_user 1, user 2, user 3',
                reply_markup=self.MatcherResponseKeyboard())
            self.assertEqual(1, session.query(Request).count())
            request = session.query(Request).first()

            # First user accepted.
            self._reset_message(context)
            type(context).sender = PropertyMock(return_value=other_users[0])
            type(context.update.callback_query.message).message_id = PropertyMock(return_value=request.message_id)
            broadcasts.on_recall_join(context)
            context.update.callback_query.edit_message_text.assert_called_once_with(
                text='recall_from_sender\n\nrecall_joined_user 1\nrecall_not_answered_user 2, user 3',
                reply_markup=self.MatcherResponseKeyboard())
            self.assertEqual(1, session.query(Response).count())

            # Second user declined.
            self._reset_message(context)
            type(context).sender = PropertyMock(return_value=other_users[1])
            broadcasts.on_recall_decline(context)
            context.update.callback_query.edit_message_text.assert_called_once_with(
                text='recall_from_sender\n\nrecall_joined_user 1\nrecall_declined_user 2\nrecall_not_answered_user 3',
                reply_markup=self.MatcherResponseKeyboard())
            self.assertEqual(2, session.query(Response).count())

            # First user declined too.
            self._reset_message(context)
            type(context).sender = PropertyMock(return_value=other_users[0])
            broadcasts.on_recall_decline(context)
            context.update.callback_query.edit_message_text.assert_called_once_with(
                text='recall_from_sender\n\nrecall_declined_user 1, user 2\nrecall_not_answered_user 3',
                reply_markup=self.MatcherResponseKeyboard())
            self.assertEqual(2, session.query(Response).count())

            # Message became obsolete and can not be updated.
            self._reset_message(context)
            context.update.callback_query.edit_message_text.side_effect = TelegramError('')
            broadcasts.on_recall_decline(context)
            context.update.callback_query.edit_message_text.assert_called_once_with(
                text='recall_from_sender\n\nrecall_declined_user 1, user 2\nrecall_not_answered_user 3',
                reply_markup=self.MatcherResponseKeyboard())
            context.send_response_message.assert_called_once_with('invalid_request_user 1')
            self.assertEqual(2, session.query(Response).count())
