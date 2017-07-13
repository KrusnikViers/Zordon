from telegram import CallbackQuery
from unittest import TestCase
from unittest.mock import create_autospec, MagicMock, PropertyMock

from app.definitions import superuser_login
from app.handlers.utils import *


class TestCommonHandlers(TestCase):
    def setUp(self):
        User.delete().execute()


class TestUserKeyboard(TestCommonHandlers):
    def _check_keyboard_expectations(self, keyboard, expected_buttons):
        self.assertEqual(len(keyboard), len(expected_buttons))
        for row_index in range(0, len(keyboard)):
            self.assertEqual(len(keyboard[row_index]), len(expected_buttons[row_index]))
            for button_index in range(0, len(keyboard[row_index])):
                self.assertEqual(keyboard[row_index][button_index].text,
                                 expected_buttons[row_index][button_index])

    def test_inactive_user_keyboard(self):
        expected_keyboard_commands = [['Ready', 'Status'], ['Activities list']]
        user = User.create(telegram_user_id=0, is_active=False)
        self._check_keyboard_expectations(build_default_keyboard(user).keyboard, expected_keyboard_commands)

    def test_usual_user_keyboard(self):
        expected_keyboard_commands = [['Do not disturb', 'Status'], ['Activities list']]
        user = User.create(telegram_user_id=0)
        self._check_keyboard_expectations(build_default_keyboard(user).keyboard, expected_keyboard_commands)

    def test_keyboard_rights_level_1(self):
        expected_keyboard_commands = [['Do not disturb', 'Status'], ['Activities list', 'Summon friends']]
        user = User.create(telegram_user_id=0, rights_level=1)
        self._check_keyboard_expectations(build_default_keyboard(user).keyboard, expected_keyboard_commands)

    def test_superuser_keyboard(self):
        expected_keyboard_commands = [['Do not disturb', 'Status'],
                                      ['Activities list', 'Summon friends', 'Full information']]
        user = User.create(telegram_user_id=0, telegram_login=superuser_login)
        self._check_keyboard_expectations(build_default_keyboard(user).keyboard, expected_keyboard_commands)


class TestPersonalCommand(TestCommonHandlers):
    def test_callback_query(self):
        update = Update(0, callback_query=create_autospec(CallbackQuery))
        user = User.create(telegram_user_id=0)
        handler = MagicMock()
        handler.return_value = None

        # Call decorator explicitly
        personal_command()(handler)(None, update, user)
        update.callback_query.answer.assert_called_once_with()
        handler.assert_called_once_with(None, update, user)

    def test_user_undefined(self):
        update = MagicMock()
        type(update.effective_user).id = PropertyMock(return_value=12345)
        type(update.effective_user).name = PropertyMock(return_value='username')
        handler = MagicMock()
        handler.return_value = None

        # Call decorator explicitly
        personal_command()(handler)(None, update)
        self.assertTrue(handler.called)
        self.assertTrue(User.get(User.telegram_user_id == 12345, User.telegram_login == 'username'))

    def test_not_enough_rights(self):
        user = MagicMock()
        update = MagicMock()
        bot = MagicMock()
        handler = MagicMock()
        user.has_right.return_value = False

        personal_command('su_full_information')(handler)(bot, update, user)
        user.has_right.assert_any_call('su_full_information')
        self.assertTrue(user.send_message.called)
        self.assertFalse(handler.called)
