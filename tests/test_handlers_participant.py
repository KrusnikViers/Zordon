from app.handlers.participant import *
from .base_test import BaseTestCase


class TestParticipantHandlers(BaseTestCase):
    def setUp(self):
        super(TestParticipantHandlers, self).setUp()
        self.user_1 = User.create(telegram_user_id=1, rights_level=1)
        self.activity = Activity.create(name='test', owner=self.user_1)
        self.subscription = Subscription.create(activity=self.activity, user=self.user_1)

    def test_summon_basic(self):
        on_summon(self._mm_bot, self._mm_update, self.user_1)

    def test_summon_without_subscription(self):
        Subscription.delete().execute()
        self.call_handler_with_mock(on_summon, self.user_1)
        self._mm_bot.send_message.assert_called_once_with(self.user_1.telegram_user_id,
                                                          text=self.Any(),
                                                          parse_mode='Markdown',
                                                          reply_markup=self.KeyboardMatcher([
                                                              ['p_summon test']
                                                          ]))

    def test_summon_no_activities(self):
        Activity.delete().execute()
        on_summon(self._mm_bot, self._mm_update, self.user_1)

    def test_summon_with_data_basic(self):
        # Simple subscriber
        s_user = User.create(telegram_user_id=12345)
        Subscription.create(user=s_user, activity=self.activity)
        self.set_callback_data(self.user_1, 'p_summon ' + self.activity.name)
        on_summon_with_data(self._mm_bot, self._mm_update)

    def test_summon_with_data_non_existing_activity(self):
        self.set_callback_data(self.user_1, 'p_summon non_existing')
        on_summon_with_data(self._mm_bot, self._mm_update)

    def test_accept_basic(self):
        self.set_callback_data(self.user_1, 'p_accept ' + self.activity.name)
        on_accept_now_with_data(self._mm_bot, self._mm_update)

    def test_accept_later_basic(self):
        self.set_callback_data(self.user_1, 'p_accept_later ' + self.activity.name)
        on_accept_later_with_data(self._mm_bot, self._mm_update)

    def test_decline_basic(self):
        self.set_callback_data(self.user_1, 'p_decline ' + self.activity.name)
        on_decline_with_data(self._mm_bot, self._mm_update)

    def test_accept_bad_activity_name(self):
        self.set_callback_data(self.user_1, 'p_accept non_existing')
        on_accept_now_with_data(self._mm_bot, self._mm_update)

    def test_accept_later_bad_activity_name(self):
        self.set_callback_data(self.user_1, 'p_accept_later non_existing')
        on_accept_later_with_data(self._mm_bot, self._mm_update)

    def test_decline_bad_activity_name(self):
        self.set_callback_data(self.user_1, 'p_decline non_existing')
        on_decline_with_data(self._mm_bot, self._mm_update)

