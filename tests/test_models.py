from unittest import TestCase
from unittest.mock import create_autospec

from app.handlers.common import commands_map
from app.models import *


class TestModels(TestCase):
    def setUp(self):
        Activity.delete().execute()
        User.delete().execute()


class TestUserModel(TestModels):
    def test_rights_usual(self):
        allowed_commands = {'start', 'status', 'activate', 'deactivate', 'cancel', 'activity_list', 'subscribe',
                            'unsubscribe', 'join', 'later', 'decline'}
        user = User.create(telegram_user_id=0)
        for command in commands_map:
            self.assertEqual(user.has_right(command), (command in allowed_commands), msg=command)

    def test_rights_level_1(self):
        allowed_commands = {'start', 'status', 'activate', 'deactivate', 'cancel', 'activity_list', 'activity_add',
                            'activity_rem', 'subscribe', 'unsubscribe', 'summon', 'join', 'later', 'decline'}
        user = User.create(telegram_user_id=0, rights_level=1)
        for command in commands_map:
            self.assertEqual(user.has_right(command), (command in allowed_commands), msg=command)

    def test_rights_superuser(self):
        user = User.create(telegram_user_id=0, telegram_login=superuser_login)
        for command in commands_map:
            self.assertTrue(user.has_right(command), msg=command)

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


class TestActivityModel(TestModels):
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
