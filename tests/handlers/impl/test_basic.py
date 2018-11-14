from unittest.mock import MagicMock, PropertyMock

from tests.base import InBotTestCase, ScopedSession
from app.models.all import *
from app.handlers.impl import basic


class TestBasicHandlers(InBotTestCase):
    def test_group_changes(self):
        with ScopedSession(self.connection) as session:
            group = Group(id=0, name='test')
            session.add(group)

            leaving_user = User(id=0, name='Leaving one')
            leaving_user.groups.append(group)
            session.add(leaving_user)

            new_user_login = User(id=1, name='New one 1', login='new_one_1', is_known=True)
            session.add(new_user_login)
            new_user_name = User(id=2, name='New one 2')
            session.add(new_user_name)

            context = MagicMock()
            type(context).group = PropertyMock(return_value=group)
            type(context).sender = PropertyMock(return_value=new_user_login)
            type(context).users_joined = PropertyMock(return_value=[new_user_login, new_user_name])
            type(context).user_left = PropertyMock(return_value=leaving_user)

            basic.process_group_changes(context)

        context.send_response_message.assert_any_call('greet_known_New one 1')
        context.send_response_message.assert_any_call('greet_new_New one 2')
        context.send_response_message.assert_any_call('farewell_Leaving one')
        self.assertEqual(3, context.send_response_message.call_count)

    def test_huge_ids(self):
        huge_id = 1 << 62

        with ScopedSession(self.connection) as session:
            group = Group(id=huge_id, name='test')
            session.add(group)
            new_user = User(id=huge_id + 1, name='New user')
            session.add(new_user)

            context = MagicMock()
            type(context).group = PropertyMock(return_value=group)
            type(context).sender = PropertyMock(return_value=new_user)
            basic.process_group_changes(context)

        context.send_response_message.assert_any_call('greet_new_New user')
        self.assertEqual(1, context.send_response_message.call_count)

        with ScopedSession(self.connection) as session:
            self.assertEqual(huge_id, session.query(Group).first().id)
            self.assertEqual(huge_id + 1, session.query(User).first().id)

    def test_help_or_start_private(self):
        context = MagicMock()
        type(context).group = PropertyMock(return_value=None)
        basic.on_help_or_start(context)
        context.send_response_message.assert_called_once_with('Zordon v3.0.0_help_for_private')

    def test_help_or_start_group(self):
        context = MagicMock()
        basic.on_help_or_start(context)
        context.send_response_message.assert_called_once_with('Zordon v3.0.0_help_for_group')

    def test_click_here(self):
        context = MagicMock()
        basic.on_click_here(context)
        context.send_response_message.assert_called_once_with(_('rdr2_easter_egg'))
