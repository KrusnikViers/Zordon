from unittest.mock import patch, MagicMock

from app.models import *
from tests.base_test import BaseTestCase


# Setting up handlers mocks
class HandlersMocker:
    def __enter__(self):
        handlers_to_mock = [
            ('activity', 'on_list'),
            ('activity', 'on_new_with_data'),
            ('participant', 'on_summon'),
            ('superuser', 'on_full_information'),
            ('user', 'on_status'),
            ('user', 'on_activate'),
            ('user', 'on_deactivate'),
            ('user', 'on_cancel'),
            ('user', 'on_report'),
            ('user', 'on_report_with_data'),
        ]
        mocked_handlers = {
            (x[0] + '_' + x[1]):
                patch('app.handlers.' + x[0] + '.' + x[1], MagicMock()).start() for x in handlers_to_mock
        }
        return mocked_handlers

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestMessagesHandlers(BaseTestCase):
    def setUp(self):
        super(TestMessagesHandlers, self).setUp()

    def _check_invoked_times(self, value, handlers):
        count = 0
        for mock in handlers.values():
            if mock.called:
                count += 1
        self.assertEqual(value, count)

    def test_message_routing_none(self):
        with HandlersMocker() as mockers:
            import app.handlers.messages as h_messages

            user = User.create(telegram_user_id=0)
            self.set_message_text('Not alias')
            h_messages.message_handler(self._mm_bot, self._mm_update, user)
            self._check_invoked_times(0, mockers)

    def test_message_routing_activity_new(self):
        with HandlersMocker() as mockers:
            import app.handlers.messages as h_messages
            user = User.create(telegram_user_id=0, pending_action=pending_user_actions['a_new'])
            self.set_message_text('Not alias')
            h_messages.message_handler(self._mm_bot, self._mm_update, user)
            self._check_invoked_times(1, mockers)
            mockers['activity_on_new_with_data'].assert_called_once_with(self._mm_bot, self._mm_update, user)

    def test_message_routing_report(self):
        with HandlersMocker() as mockers:
            import app.handlers.messages as h_messages
            user = User.create(telegram_user_id=0, pending_action=pending_user_actions['u_report'])
            self.set_message_text('Not alias')
            h_messages.message_handler(self._mm_bot, self._mm_update, user)
            self._check_invoked_times(1, mockers)
            mockers['user_on_report_with_data'].assert_called_once_with(self._mm_bot, self._mm_update, user)

    def test_message_routing_keyboard_aliases(self):
        with HandlersMocker() as mockers:
            import app.handlers.messages as h_messages
            from app.handlers.misc.keyboard import UserKeyboard
            user = User.create(telegram_user_id=0, telegram_login=superuser_login)
            markup = UserKeyboard(user)  # Superuser keyboard has the biggest number of controls
            count = 0  # Each keyboard button should add unique call
            for row in markup.keyboard:
                for button in row:
                    self.set_message_text(button.text)
                    h_messages.message_handler(self._mm_bot, self._mm_update, user)
                    count += 1
                    self._check_invoked_times(count, mockers)
