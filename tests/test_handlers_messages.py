from .base_test import BaseTestCase
from unittest.mock import patch, create_autospec, MagicMock

from app.models import *


# Setting up handlers mocks
_mock_handlers = dict()
def _create_mock(handler_module: str, handler_name: str):
    _mock_handlers[handler_module + '_' + handler_name] = patch(
        'app.handlers.' + handler_module + '.' + handler_name, autospec=True).start()

_create_mock('activity', 'on_list')
_create_mock('activity', 'on_new_with_data')
_create_mock('participant', 'on_summon')
_create_mock('superuser', 'on_full_information')
_create_mock('user', 'on_status')
_create_mock('user', 'on_activate')
_create_mock('user', 'on_deactivate')
_create_mock('user', 'on_cancel')
_create_mock('user', 'on_report')
_create_mock('user', 'on_report_with_data')

import app.handlers.messages as h_messages
import app.handlers.utils as h_utils


class TestMessagesHandlers(BaseTestCase):
    def setUp(self):
        super(TestMessagesHandlers, self).setUp()
        for mock in _mock_handlers.values():
            mock.reset_mock()

    def _check_invoked_times(self, value):
        count = 0
        for mock in _mock_handlers.values():
            if mock.called:
                count += 1
        self.assertEqual(value, count)

    def test_message_routing_none(self):
        user = User.create(telegram_user_id=0)
        self.set_message_text('Not alias')
        h_messages.message_handler(self._mm_bot, self._mm_update, user)
        self._check_invoked_times(0)

    def test_message_routing_activity_new(self):
        user = User.create(telegram_user_id=0, pending_action=pending_user_actions['a_new'])
        self.set_message_text('Not alias')
        h_messages.message_handler(self._mm_bot, self._mm_update, user)
        self._check_invoked_times(1)
        _mock_handlers['activity_on_new_with_data'].assert_called_once_with(self._mm_bot, self._mm_update, user)

    def test_message_routing_report(self):
        user = User.create(telegram_user_id=0, pending_action=pending_user_actions['u_report'])
        self.set_message_text('Not alias')
        h_messages.message_handler(self._mm_bot, self._mm_update, user)
        self._check_invoked_times(1)
        _mock_handlers['user_on_report_with_data'].assert_called_once_with(self._mm_bot, self._mm_update, user)

    def test_message_routing_keyboard_aliases(self):
        user = User.create(telegram_user_id=0, telegram_login=superuser_login)
        markup = h_utils.build_default_keyboard(user)  # Superuser keyboard has the biggest number of controls
        count = 0  # Each keyboard button should add unique call
        for row in markup.keyboard:
            for button in row:
                self.set_message_text(button.text)
                h_messages.message_handler(self._mm_bot, self._mm_update, user)
                count += 1
                self._check_invoked_times(count)
