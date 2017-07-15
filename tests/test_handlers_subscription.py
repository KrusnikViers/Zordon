from app.handlers.subscription import *
from .base_test import BaseTestCase


class TestParticipantHandlers(BaseTestCase):
    def setUp(self):
        super(TestParticipantHandlers, self).setUp()
        self.user_1 = User.create(telegram_user_id=1, rights_level=1)
        self.activity = Activity.create(name='test', owner=self.user_1)

    def test_new_basic(self):
        on_new(self._mm_bot, self._mm_update, self.user_1)

    def test_new_no_activities(self):
        Activity.delete().execute()
        on_new(self._mm_bot, self._mm_update, self.user_1)

    def test_new_with_data_basic(self):
        another_user = User.create(telegram_user_id=12345)
        Participant.create(activity=self.activity, user=another_user, report_time=datetime.datetime.now())
        self.set_callback_data(self.user_1.telegram_user_id, 's_new ' + self.activity.name)
        on_new_with_data(self._mm_bot, self._mm_update)

    def test_new_with_data_wrong_activity(self):
        self.set_callback_data(self.user_1.telegram_user_id, 's_new non_existing')
        on_new_with_data(self._mm_bot, self._mm_update)

    def test_delete_basic(self):
        Subscription.create(activity=self.activity, user=self.user_1)
        on_delete(self._mm_bot, self._mm_update, self.user_1)

    def test_delete_empty(self):
        on_delete(self._mm_bot, self._mm_update, self.user_1)

    def test_delete_with_data_basic(self):
        Subscription.create(activity=self.activity, user=self.user_1)
        self.set_callback_data(self.user_1.telegram_user_id, 's_delete ' + self.activity.name)
        on_delete_with_data(self._mm_bot, self._mm_update)

    def test_delete_with_data_wrong_activity(self):
        Subscription.create(activity=self.activity, user=self.user_1)
        self.set_callback_data(self.user_1.telegram_user_id, 's_delete non_existing')
        on_delete_with_data(self._mm_bot, self._mm_update)
        self.assertTrue(Subscription.select((Subscription.activity == self.activity) &
                                            (Subscription.user == self.user_1)).exists())
