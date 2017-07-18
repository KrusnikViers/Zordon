from unittest.mock import create_autospec

from app.models import *
from .base_test import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_rights_usual(self):
        allowed_commands = {'u_status', 'u_activate', 'u_deactivate', 'u_cancel', 'a_list', 's_new', 's_delete',
                            'p_accept', 'p_accept_later', 'p_decline', 'u_report', 'c_abort'}
        user = User.create(telegram_user_id=0)
        for command in commands_set:
            self.assertEqual(user.has_right_to(command), (command in allowed_commands), msg=command)

    def test_rights_level_1(self):
        allowed_commands = {'u_status', 'u_activate', 'u_deactivate', 'u_cancel', 'a_list', 'a_new', 'a_delete',
                            's_new', 's_delete', 'p_summon', 'p_accept', 'p_accept_later', 'p_decline', 'u_report',
                            'c_abort'}
        user = User.create(telegram_user_id=0, rights_level=1)
        for command in commands_set:
            self.assertEqual(user.has_right_to(command), (command in allowed_commands), msg=command)

    def test_rights_superuser(self):
        user = User.create(telegram_user_id=0, telegram_login=superuser_login)
        for command in commands_set:
            self.assertTrue(user.has_right_to(command), msg=command)

    def test_send_message_basic(self):
        bot_mock = create_autospec(Bot)
        user = User.create(telegram_user_id=12345)
        user.send_message(bot_mock, text='test_text', reply_markup='test_markup')
        bot_mock.send_message.assert_called_once_with(chat_id=12345,
                                                      text='test_text',
                                                      reply_markup='test_markup',
                                                      parse_mode='Markdown')
        self.assertFalse(user.is_disabled_chat)

    def test_send_message_with_exception(self):
        bot_mock = create_autospec(Bot)
        bot_mock.send_message.side_effect = TelegramError('')
        user = User.create(telegram_user_id=12345)
        user.send_message(bot_mock, text='test_text', reply_markup='test_markup')
        bot_mock.send_message.assert_called_once_with(chat_id=12345,
                                                      text='test_text',
                                                      reply_markup='test_markup',
                                                      parse_mode='Markdown')
        self.assertTrue(user.is_disabled_chat)

    def test_send_message_to_superuser(self):
        bot_mock = create_autospec(Bot)
        user = User.create(telegram_user_id=12345)
        superuser = User.create(telegram_user_id=123, telegram_login=superuser_login)
        user.send_message_to_superuser(bot_mock, text='test_text')
        bot_mock.send_message.assert_called_once_with(chat_id=123,
                                                      text='test_text',
                                                      parse_mode='Markdown')
        self.assertFalse(user.is_disabled_chat)
        self.assertFalse(superuser.is_disabled_chat)


class TestActivityModel(BaseTestCase):
    def test_try_to_create_basic(self):
        user = User.create(telegram_user_id=0)
        result = Activity.try_to_create('Correct name', user)[0]
        self.assertNotEqual(None, result)
        self.assertEqual('Correct name', result.name)
        self.assertEqual(user, result.owner)

    def test_try_to_create_wrong_length(self):
        user = User.create(telegram_user_id=0)
        result = Activity.try_to_create('Too many letters obviously', user)[0]
        self.assertEqual(None, result)

    def test_try_to_create_empty(self):
        user = User.create(telegram_user_id=0)
        result = Activity.try_to_create('    ', user)[0]
        self.assertEqual(None, result)

    def test_try_to_create_bad_characters(self):
        user = User.create(telegram_user_id=0)
        result = Activity.try_to_create('Why, mr Andersen?', user)[0]
        self.assertEqual(None, result)

    def test_try_to_create_already_exists(self):
        user = User.create(telegram_user_id=0)
        activity = Activity.try_to_create('Im fine', user)[0]
        self.assertNotEqual(None, activity)
        result = Activity.try_to_create('Im fine', user)[0]
        self.assertEqual(None, result)

    def test_has_right_to_remove_owner(self):
        user = User.create(telegram_user_id=0)
        superuser = User.create(telegram_user_id=1, telegram_login=superuser_login)
        another_user = User.create(telegram_user_id=2)
        activity = Activity.try_to_create('Correct name', user)[0]
        self.assertFalse(activity.has_right_to_remove(user))
        self.assertTrue(activity.has_right_to_remove(superuser))
        self.assertFalse(activity.has_right_to_remove(another_user))

    def test_try_to_get_basic(self):
        user = User.create(telegram_user_id=0)
        activity = Activity.create(name='TestActivity', owner=user)

        result, error = Activity.try_to_get('TestActivity')
        self.assertEqual(activity, result)
        self.assertFalse(error)

    def test_try_to_get_not_existing(self):
        result, error = Activity.try_to_get('NonExistingActivity')
        self.assertEqual(None, result)
        self.assertTrue(error)


class TestParticipantModel(BaseTestCase):
    def setUp(self):
        super(TestParticipantModel, self).setUp()
        self.users = [User.create(telegram_user_id=i) for i in range(0, 15) if i != 5]
        self.activities = [Activity.create(name=str(i), owner=self.users[i]) for i in range(0, 4)]

    def test_clear_inactive(self):
        cooldown_delta = datetime.timedelta(minutes=cooldown_time_minutes + 5)
        is_accepted = True
        for user in self.users:
            is_accepted = not is_accepted
            report_time = datetime.datetime.now() - cooldown_delta + datetime.timedelta(minutes=user.telegram_user_id)
            Participant.create(user=user, activity=self.activities[0], is_accepted=is_accepted, report_time=report_time)
        self.assertEqual(14, Participant.select().count())
        Participant.clear_inactive()
        self.assertEqual(9, Participant.select().count())

    def test_select_participants(self):
        for user in self.users:
            case = user.telegram_user_id % (len(self.activities) + 1)
            if case < len(self.activities):
                Participant.create(activity=self.activities[case], user=user)
        # Only 10th user - zero user does not count itself
        self.assertEqual(1, Participant.select_participants_for_activity(self.activities[0], self.users[0]).count())
        # 1st, 6th and 11th users
        self.assertEqual(3, Participant.select_participants_for_activity(self.activities[1], self.users[0]).count())

    def test_select_subscribers(self):
        for user in self.users:
            activity = self.activities[user.telegram_user_id % len(self.activities)]
            taking_part = user.telegram_user_id % 3 == 0
            Subscription.create(activity=activity, user=user)
            if taking_part:
                Participant.create(activity=activity, user=user)

        # 4th and 8th users (zero and 12 users are already participants)
        self.assertEqual(2, Participant.select_subscribers_for_activity(self.activities[0]).count())
        # 1 and 13 (without 9)
        self.assertEqual(2, Participant.select_subscribers_for_activity(self.activities[1]).count())
        # 2, 10 and 14 (without 6)
        self.assertEqual(3, Participant.select_subscribers_for_activity(self.activities[2]).count())
        # 7 and 11 (without 3) - and check it for the last selection
        self.assertEqual(2, Participant.select_subscribers_for_activity(self.activities[3]).count())
        for participant in Participant.select_subscribers_for_activity(self.activities[3]):
            self.assertTrue(participant.telegram_user_id in {7, 11})

    def test_response_to_summon(self):
        prev = Participant.create(activity=self.activities[0], user=self.users[1])
        cur = Participant.create(activity=self.activities[0], user=self.users[0])
        bot_mock = create_autospec(Bot)

        Participant.response_to_summon(bot_mock, self.users[0], self.activities[0], 'p_decline')
        bot_mock.send_message.assert_called_once_with(chat_id=1, parse_mode='Markdown', text=' declined summon for *0*')
        cur = Participant.get(activity=self.activities[0], user=self.users[0])
        self.assertFalse(cur.is_accepted)
