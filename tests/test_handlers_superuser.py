from app.handlers.superuser import *
from .base_test import BaseTestCase


class TestParticipantHandlers(BaseTestCase):
    def setUp(self):
        super(TestParticipantHandlers, self).setUp()
        self.superuser = User.create(telegram_user_id=1, telegram_login=superuser_login)
        self.user_0 = User.create(telegram_user_id=10)
        self.user_1 = User.create(telegram_user_id=20, rights_level=1)

    def test_full_information_basic(self):
        activity = Activity.create(name='test', owner=self.user_0)
        Subscription.create(activity=activity, user=self.user_1)
        Participant.create(activity=activity, user=self.superuser)
        on_full_information(self._mm_bot, self._mm_update, self.superuser)

    def test_promote_basic(self):
        self.set_callback_data(self.superuser, 'su_promote')
        on_promote(self._mm_bot, self._mm_update)

    def test_promote_no_users(self):
        self.set_callback_data(self.superuser, 'su_promote')
        User.delete().execute()
        on_promote(self._mm_bot, self._mm_update)

    def test_promote_with_data_basic(self):
        self.set_callback_data(self.superuser, 'su_promote ' + str(self.user_0.telegram_user_id))
        on_promote_with_data(self._mm_bot, self._mm_update)

    def test_promote_with_data_again(self):
        self.set_callback_data(self.superuser, 'su_promote ' + str(self.user_1.telegram_user_id))
        on_promote_with_data(self._mm_bot, self._mm_update)

    def test_demote_basic(self):
        self.set_callback_data(self.superuser, 'su_demote')
        on_demote(self._mm_bot, self._mm_update)

    def test_demote_no_users(self):
        self.set_callback_data(self.superuser, 'su_demote')
        User.delete().execute()
        on_demote(self._mm_bot, self._mm_update)

    def test_demote_with_data_basic(self):
        self.set_callback_data(self.superuser, 'su_demote ' + str(self.user_1.telegram_user_id))
        on_demote_with_data(self._mm_bot, self._mm_update)

    def test_demote_with_data_again(self):
        self.set_callback_data(self.superuser, 'su_demote ' + str(self.user_0.telegram_user_id))
        on_demote_with_data(self._mm_bot, self._mm_update)
