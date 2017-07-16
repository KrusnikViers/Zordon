from telegram import CallbackQuery
from unittest.mock import create_autospec, MagicMock

from app.definitions import superuser_login
from app.handlers.utils import *
from .base_test import BaseTestCase


class TestUserKeyboard(BaseTestCase):
    def _check_keyboard_expectations(self, keyboard, expected_buttons):
        self.assertEqual(len(keyboard), len(expected_buttons))
        for row_index in range(0, len(keyboard)):
            self.assertEqual(len(keyboard[row_index]), len(expected_buttons[row_index]))
            for button_index in range(0, len(keyboard[row_index])):
                self.assertEqual(keyboard[row_index][button_index].text,
                                 expected_buttons[row_index][button_index])

    def test_inactive_user_keyboard(self):
        expected_keyboard_commands = [['Ready', 'Status'], ['Activities list', 'Report bug']]
        user = User.create(telegram_user_id=0, is_active=False)
        self._check_keyboard_expectations(build_default_keyboard(user).keyboard, expected_keyboard_commands)

    def test_usual_user_keyboard(self):
        expected_keyboard_commands = [['Do not disturb', 'Status'], ['Activities list', 'Report bug']]
        user = User.create(telegram_user_id=0)
        self._check_keyboard_expectations(build_default_keyboard(user).keyboard, expected_keyboard_commands)

    def test_keyboard_rights_level_1(self):
        expected_keyboard_commands = [['Do not disturb', 'Status'], ['Activities list', 'Summon friends', 'Report bug']]
        user = User.create(telegram_user_id=0, rights_level=1)
        self._check_keyboard_expectations(build_default_keyboard(user).keyboard, expected_keyboard_commands)

    def test_superuser_keyboard(self):
        expected_keyboard_commands = [['Do not disturb', 'Status'],
                                      ['Activities list', 'Summon friends', 'Report bug', 'Full information']]
        user = User.create(telegram_user_id=0, telegram_login=superuser_login)
        self._check_keyboard_expectations(build_default_keyboard(user).keyboard, expected_keyboard_commands)


class TestInlineKeyboard(BaseTestCase):
    def test_basic_keyboard(self):
        source = [[('t11', 'cb11'), ('t12', 'cb12')], [('t21', 'c21')]]
        result = build_inline_keyboard(source)
        self.assertTrue(isinstance(result, InlineKeyboardMarkup))
        self.assertEqual(len(source), len(result.inline_keyboard))
        for i in range(0, len(source)):
            self.assertEqual(len(source[i]), len(result.inline_keyboard[i]))
            for j in range(0, len(source[i])):
                self.assertTrue(isinstance(result.inline_keyboard[i][j], InlineKeyboardButton))
                self.assertEqual(source[i][j][0], result.inline_keyboard[i][j].text)
                self.assertEqual(source[i][j][1], result.inline_keyboard[i][j].callback_data)


class TestSummonResponseKeyboard(BaseTestCase):
    def test_basic_keyboard(self):
        result = build_summon_response_keyboard('activity_name')
        self.assertTrue(isinstance(result, InlineKeyboardMarkup))
        self.assertEqual(1, len(result.inline_keyboard))
        self.assertEqual(3, len(result.inline_keyboard[0]))

        expected = ['p_accept activity_name', 'p_accept_later activity_name', 'p_decline activity_name']
        for i in range(0, 3):
            self.assertEqual(expected[i], result.inline_keyboard[0][i].callback_data)


class TestEditCallbackMessage(BaseTestCase):
    def test_empty_callback(self):
        edit_callback_message(self._mm_update, text='Some text')

    def test_basic_callback(self):
        self._mm_update.callback_query = MagicMock()
        edit_callback_message(self._mm_update, text='Some text', reply_markup='Markup')
        self._mm_update.callback_query.edit_message_text.assert_called_once_with(text='Some text',
                                                                                 parse_mode='Markdown')
        self._mm_update.callback_query.edit_message_reply_markup.assert_called_once_with(reply_markup='Markup')


class TestPersonalCommand(BaseTestCase):
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
        self._mm_update.effective_user = MagicMock()
        self._mm_update.effective_user.id = 12345
        self._mm_update.effective_user.name = 'username'
        handler = MagicMock()
        handler.return_value = None

        # Call decorator explicitly
        personal_command()(handler)(None, self._mm_update)
        self.assertTrue(handler.called)
        self.assertTrue(User.get(User.telegram_user_id == 12345, User.telegram_login == 'username'))

    def test_user_login_outdated(self):
        user = User.create(telegram_user_id=12345, telegram_login='new_one')
        self.set_callback_data(user, 'what a data')
        user.telegram_login = 'Somehow_stored_old_login'
        user.save()
        self.assertTrue(User.get(User.telegram_user_id == 12345, User.telegram_login == 'Somehow_stored_old_login'))
        handler = MagicMock()
        handler.return_value = None

        # Call decorator explicitly
        personal_command()(handler)(self._mm_bot, self._mm_update)
        self.assertTrue(User.get(User.telegram_user_id == 12345, User.telegram_login == 'new_one'))

    def test_not_enough_rights(self):
        user = MagicMock()
        handler = MagicMock()
        user.has_right_to.return_value = False

        personal_command('su_full_information')(handler)(self._mm_bot, self._mm_update, user)
        user.has_right_to.assert_any_call('su_full_information')
        self.assertTrue(user.send_message.called)
        self.assertFalse(handler.called)
