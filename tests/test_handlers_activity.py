from unittest.mock import MagicMock

from .base_test import BaseTestCase

from app.handlers.activity import *


class TestActivityHandlers(BaseTestCase):
    def setUp(self):
        super(TestActivityHandlers, self).setUp()
        self.user_1 = User.create(telegram_user_id=1, rights_level=1)

    def test_list_basic(self):
        activity = Activity.create(name='test', owner=self.user_1)
        Subscription.create(activity=activity, user=self.user_1)
        on_list(self._mm_bot, self._mm_update, self.user_1)

    def test_new_basic(self):
        on_new(self._mm_bot, self._mm_update, self.user_1)

    def test_new_with_data_basic(self):
        self._mm_update.message = MagicMock()
        self._mm_update.message.text = 'test_name'
        on_new_with_data(self._mm_bot, self._mm_update, self.user_1)
        Activity.get(name='test_name', owner=self.user_1)

    def test_delete_basic(self):
        Activity.create(name='test', owner=self.user_1)
        on_delete(self._mm_bot, self._mm_update, self.user_1)

    def test_delete_with_data_basic(self):
        Activity.create(name='test', owner=self.user_1)
        self._mm_update.callback_query = MagicMock()
        self._mm_update.callback_query.data = 'a_delete test'
        self._mm_update.effective_user = MagicMock()
        self._mm_update.effective_user.id = self.user_1.telegram_user_id

        on_delete_with_data(self._mm_bot, self._mm_update)
        self.assertEqual(0, Activity.select().where(Activity.name == 'test').count())
