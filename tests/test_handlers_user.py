from unittest.mock import call

from app.handlers.user import *
from .base_test import BaseTestCase


class TestParticipantHandlers(BaseTestCase):
    def setUp(self):
        super(TestParticipantHandlers, self).setUp()
        self.superuser = User.create(telegram_user_id=1, telegram_login=superuser_login)
        self.user_active = User.create(telegram_user_id=10, is_active=True)
        self.user_1_passive = User.create(telegram_user_id=20, rights_level=1, is_active=False)

    def test_status_basic(self):
        self.call_handler_with_mock(on_status, self.user_active)

    def test_status_rights_level_1(self):
        self.call_handler_with_mock(on_status, self.user_1_passive)

    def test_status_superuser(self):
        self.call_handler_with_mock(on_status, self.superuser)

    def test_activate_basic(self):
        self.call_handler_with_mock(on_activate, self.user_1_passive)

    def test_activate_again(self):
        self.call_handler_with_mock(on_activate, self.user_active)

    def test_activate_with_supressed_summons(self):
        activity = Activity.create(name='act', owner=self.superuser)
        another_activity = Activity.create(name='another', owner=self.superuser)
        Subscription.create(activity=activity, user=self.user_1_passive)
        Participant.create(activity=activity, user=self.superuser, report_time=datetime.datetime.now())
        Participant.create(activity=activity, user=self.user_active, report_time=datetime.datetime.now())
        self.call_handler_with_mock(on_activate, self.user_1_passive)
        # Mode change message and one invite to activity
        self._mm_bot.send_message.assert_has_calls([
            call(self.user_1_passive.telegram_user_id, parse_mode='Markdown', text=self.Any(),
                 reply_markup=self.KeyboardMatcher([['p_accept act', 'p_accept_later act', 'p_decline act']])),
            call(self.user_1_passive.telegram_user_id, parse_mode='Markdown', text=self.Any(),
                 reply_markup=self.Any())
        ])
        self.assertEqual(2, self._mm_bot.send_message.call_count)

    def test_deactivate_basic(self):
        self.call_handler_with_mock(on_deactivate, self.user_active)

    def test_deactivate_again(self):
        self.call_handler_with_mock(on_deactivate, self.user_1_passive)

    def test_cancel_basic(self):
        self.user_active.pending_action = pending_user_actions['a_new']
        self.user_active.save()
        self.call_handler_with_mock(on_cancel, self.user_active)

    def test_cancel_again(self):
        self.call_handler_with_mock(on_cancel, self.user_active)

    def test_report_basic(self):
        self.call_handler_with_mock(on_report, self.user_active)

    def test_report_with_other_pending(self):
        self.user_active.pending_action = pending_user_actions['a_new']
        self.user_active.save()
        self.call_handler_with_mock(on_report, self.user_active)

    def test_report_with_data_basic(self):
        self.set_message_text('Report message')
        self.call_handler_with_mock(on_report_with_data, self.user_active)
