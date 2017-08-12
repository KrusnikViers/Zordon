from unittest.mock import create_autospec
from telegram import Bot, TelegramError

from app.definitions import commands_set, superuser_login
from app.models.user import User
from tests.base_test import BaseTestCase


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
                                                      reply_markup='test_markup')
        self.assertFalse(user.is_disabled_chat)

    def test_send_message_with_exception(self):
        bot_mock = create_autospec(Bot)
        bot_mock.send_message.side_effect = TelegramError('')
        user = User.create(telegram_user_id=12345)
        user.send_message(bot_mock, text='test_text', reply_markup='test_markup')
        bot_mock.send_message.assert_called_once_with(chat_id=12345,
                                                      text='test_text',
                                                      reply_markup='test_markup')
        self.assertTrue(user.is_disabled_chat)

    def test_send_message_to_superuser(self):
        bot_mock = create_autospec(Bot)
        user = User.create(telegram_user_id=12345)
        superuser = User.create(telegram_user_id=123, telegram_login=superuser_login)
        user.send_message_to_superuser(bot_mock, text='test_text')
        bot_mock.send_message.assert_called_once_with(chat_id=123,
                                                      text='test_text')
        self.assertFalse(user.is_disabled_chat)
        self.assertFalse(superuser.is_disabled_chat)
