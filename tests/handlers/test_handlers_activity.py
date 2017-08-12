from app.handlers.activity import *
from tests.base_test import BaseTestCase


class TestActivityHandlers(BaseTestCase):
    def setUp(self):
        super(TestActivityHandlers, self).setUp()
        self.user_1 = User.create(telegram_user_id=1, rights_level=1, telegram_login='basic_user')

    def test_list_basic(self):
        users = [User.create(telegram_user_id=12345 + i, telegram_login=str(i)) for i in range(0, 3)]
        activities = [Activity.create(name='activity ' + str(i), owner=users[i]) for i in range(0, 3)]

        users[1].is_active = False
        users[1].save()

        Subscription.create(activity=activities[0], user=self.user_1)  # Not responded
        Subscription.create(activity=activities[1], user=self.user_1)  # Not responded
        Subscription.create(activity=activities[0], user=users[0])
        Subscription.create(activity=activities[0], user=users[1])
        Subscription.create(activity=activities[1], user=users[0])
        Subscription.create(activity=activities[1], user=users[1])
        Subscription.create(activity=activities[1], user=users[2])

        Participant.create(activity=activities[0], user=users[0])
        Participant.create(activity=activities[0], user=users[1], is_accepted=False)
        Participant.create(activity=activities[0], user=users[2])
        self.call_handler_with_mock(on_list, self.user_1)

    def test_list_empty(self):
        self.call_handler_with_mock(on_list, self.user_1)
        self._mm_bot.send_message.assert_called_once_with(self.user_1.telegram_user_id,
                                                          text=self.Any(),
                                                          reply_markup=self.KeyboardMatcher([['a_new']]))

    def test_list_keyboard(self):
        activity = Activity.create(name='test', owner=self.user_1)
        user = User.create(telegram_user_id=12345, rights_level=1)
        Subscription.create(activity=activity, user=self.user_1)
        self.call_handler_with_mock(on_list, user)
        self._mm_bot.send_message.assert_called_once_with(user.telegram_user_id,
                                                          text=self.Any(),
                                                          reply_markup=self.KeyboardMatcher([['s_new'], ['a_new']]))

    def test_list_keyboard_full(self):
        activities = [Activity.create(name=str(x), owner=self.user_1) for x in range(0, 2)]
        Subscription.create(activity=activities[0], user=self.user_1)
        self.call_handler_with_mock(on_list, self.user_1)
        self._mm_bot.send_message.assert_called_once_with(self.user_1.telegram_user_id,
                                                          text=self.Any(),
                                                          reply_markup=self.KeyboardMatcher(
                                                              [['p_summon'],
                                                               ['s_new', 's_delete'],
                                                               ['a_new', 'a_delete']]))

    def test_new_basic(self):
        on_new(self._mm_bot, self._mm_update, self.user_1)

    def test_new_another_pending(self):
        self.user_1.pending_action = pending_user_actions['u_report']
        self.user_1.save()
        on_new(self._mm_bot, self._mm_update, self.user_1)

    def test_new_with_data_basic(self):
        self.set_message_text('test_name')
        on_new_with_data(self._mm_bot, self._mm_update, self.user_1)
        Activity.get(name='test_name', owner=self.user_1)

    def test_new_with_data_bad_name(self):
        self.set_message_text('bad name?')
        on_new_with_data(self._mm_bot, self._mm_update, self.user_1)
        with self.assertRaises(Activity.DoesNotExist):
            Activity.get(name='test_name', owner=self.user_1)

    def test_delete_basic(self):
        Activity.create(name='test', owner=self.user_1)
        on_delete(self._mm_bot, self._mm_update, self.user_1)

    def test_delete_empty(self):
        on_delete(self._mm_bot, self._mm_update, self.user_1)

    def test_delete_with_data_basic(self):
        Activity.create(name='test', owner=self.user_1)
        self.set_callback_data(self.user_1, 'a_delete test')
        on_delete_with_data(self._mm_bot, self._mm_update)
        self.assertFalse(Activity.select().where(Activity.name == 'test').exists())

    def test_delete_with_data_no_activity(self):
        self.set_callback_data(self.user_1, 'a_delete non_existing')
        on_delete_with_data(self._mm_bot, self._mm_update)

    def test_delete_with_data_not_enough_rights(self):
        Activity.create(name='test', owner=self.user_1)
        usual_user = User.create(telegram_user_id=12345, rights_level=1)  # Also RL1, but not owner
        self.set_callback_data(usual_user, 'a_delete test')
        on_delete_with_data(self._mm_bot, self._mm_update)
        self.assertTrue(Activity.select().where(Activity.name == 'test').exists())
