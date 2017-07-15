from unittest.mock import MagicMock

from .base_test import BaseTestCase

from app.handlers.participant import *


class TestParticipantHandlers(BaseTestCase):
    def setUp(self):
        super(TestParticipantHandlers, self).setUp()
        self.user_1 = User.create(telegram_user_id=1, rights_level=1)
        self.activity = Activity.create(name='test', owner=self.user_1)
        self.subscription = Subscription.create(activity=self.activity, user=self.user_1)

    def test_summon_basic(self):
        on_summon(self._mm_bot, self._mm_update, self.user_1)

    def test_summon_with_data_basic(self):
        self.set_callback_data(self.user_1.telegram_user_id, 'p_summon ' + self.activity.name)
        on_summon_with_data(self._mm_bot, self._mm_update)

    def test_accept_basic(self):
        self.set_callback_data(self.user_1.telegram_user_id, 'p_accept ' + self.activity.name)
        on_accept_now_with_data(self._mm_bot, self._mm_update)

    def test_accept_later_basic(self):
        self.set_callback_data(self.user_1.telegram_user_id, 'p_accept_later ' + self.activity.name)
        on_accept_later_with_data(self._mm_bot, self._mm_update)

    def test_decline_basic(self):
        self.set_callback_data(self.user_1.telegram_user_id, 'p_decline ' + self.activity.name)
        on_decline_with_data(self._mm_bot, self._mm_update)
