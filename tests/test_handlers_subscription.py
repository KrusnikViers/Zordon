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

    def test_new_from_other_user(self):
        user_0 = User.create(telegram_user_id=10)
        another_activity = Activity.create(name='another', owner=self.user_1)
        Subscription.create(activity=another_activity, user=user_0)
        Subscription.create(activity=self.activity, user=self.user_1)
        self.call_handler_with_mock(on_new, user_0)
        self._mm_bot.send_message.assert_called_once_with(user_0.telegram_user_id,
                                                          text=self.Any(),
                                                          parse_mode='Markdown',
                                                          reply_markup=self.KeyboardMatcher([['s_new test']]))

    def test_new_with_data_basic(self):
        another_user = User.create(telegram_user_id=12345)
        Participant.create(activity=self.activity, user=another_user)
        self.set_callback_data(self.user_1, 's_new ' + self.activity.name)
        on_new_with_data(self._mm_bot, self._mm_update)

    def test_new_with_data_wrong_activity(self):
        self.set_callback_data(self.user_1, 's_new non_existing')
        on_new_with_data(self._mm_bot, self._mm_update)

    def test_delete_basic(self):
        Subscription.create(activity=self.activity, user=self.user_1)
        on_delete(self._mm_bot, self._mm_update, self.user_1)

    def test_delete_empty(self):
        on_delete(self._mm_bot, self._mm_update, self.user_1)

    def test_delete_from_other_user(self):
        user_0 = User.create(telegram_user_id=10)
        Subscription.create(activity=self.activity, user=user_0)
        self.call_handler_with_mock(on_delete, user_0)
        self._mm_bot.send_message.assert_called_once_with(user_0.telegram_user_id,
                                                          text=self.Any(),
                                                          parse_mode='Markdown',
                                                          reply_markup=self.KeyboardMatcher([['s_delete test']]))

    def test_delete_with_data_basic(self):
        Subscription.create(activity=self.activity, user=self.user_1)
        self.set_callback_data(self.user_1, 's_delete ' + self.activity.name)
        on_delete_with_data(self._mm_bot, self._mm_update)

    def test_delete_with_data_wrong_activity(self):
        Subscription.create(activity=self.activity, user=self.user_1)
        self.set_callback_data(self.user_1, 's_delete non_existing')
        on_delete_with_data(self._mm_bot, self._mm_update)
        self.assertTrue(Subscription.select((Subscription.activity == self.activity) &
                                            (Subscription.user == self.user_1)).exists())
