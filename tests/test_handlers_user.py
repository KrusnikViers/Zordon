from app.handlers.user import *
from .base_test import BaseTestCase


class TestParticipantHandlers(BaseTestCase):
    def setUp(self):
        super(TestParticipantHandlers, self).setUp()
        self.superuser = User.create(telegram_user_id=1, telegram_login=superuser_login)
        self.user_active = User.create(telegram_user_id=10, is_active=True)
        self.user_1_passive = User.create(telegram_user_id=20, rights_level=1, is_active=False)

    def test_status_basic(self):
        on_status(self._mm_bot, self._mm_update, self.superuser)

    def test_activate_basic(self):
        on_activate(self._mm_bot, self._mm_update, self.user_1_passive)

    def test_deactivate_basic(self):
        on_deactivate(self._mm_bot, self._mm_update, self.user_active)

    def test_cancel_basic(self):
        self.user_active.pending_action = pending_user_actions['a_new']
        self.user_active.save()
        on_cancel(self._mm_bot, self._mm_update, self.user_active)

    def test_report_basic(self):
        on_report(self._mm_bot, self._mm_update, self.user_active)

    def test_report_with_data_basic(self):
        self.set_message_text('Report message')
        on_report_with_data(self._mm_bot, self._mm_update, self.user_active)
