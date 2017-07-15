from unittest.mock import MagicMock

from .base_test import BaseTestCase

from app.handlers.subscription import *


class TestParticipantHandlers(BaseTestCase):
    def setUp(self):
        super(TestParticipantHandlers, self).setUp()
        self.user_1 = User.create(telegram_user_id=1, rights_level=1)
        self.activity = Activity.create(name='test', owner=self.user_1)

    def test_new_basic(self):
        on_new(self._mm_bot, self._mm_update, self.user_1)

    def test_new_with_data_basic(self):
        self.set_callback_data(self.user_1.telegram_user_id, 's_new ' + self.activity.name)
        on_new_with_data(self._mm_bot, self._mm_update)

    def test_delete_basic(self):
        Subscription.create(activity=self.activity, user=self.user_1)
        on_delete(self._mm_bot, self._mm_update, self.user_1)

    def test_delete_with_data_basic(self):
        Subscription.create(activity=self.activity, user=self.user_1)
        self.set_callback_data(self.user_1.telegram_user_id, 's_delete ' + self.activity.name)
        on_delete_with_data(self._mm_bot, self._mm_update)
