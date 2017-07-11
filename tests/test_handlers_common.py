from unittest import TestCase
from app.models import *
from app.handlers.common import commands_map, keyboard_for_user
from app.definitions import superuser_login


class TestModels(TestCase):
    def setUp(self):
        User.delete().execute()

    def _check_keyboard_expectations(self, keyboard, expected_buttons):
        self.assertEqual(len(keyboard), len(expected_buttons))
        for row_index in range(0, len(keyboard)):
            self.assertEqual(len(keyboard[row_index]), len(expected_buttons[row_index]))
            for button_index in range(0, len(keyboard[row_index])):
                self.assertEqual(keyboard[row_index][button_index].text,
                                 '/' + expected_buttons[row_index][button_index])

    def test_inactive_user_keyboard(self):
        expected_keyboard_commands = [[commands_map['activate'], commands_map['status']],
                                      [commands_map['activity_list']]]
        user = User.create(telegram_user_id=0, is_active=False)
        self._check_keyboard_expectations(keyboard_for_user(user).keyboard, expected_keyboard_commands)

    def test_usual_user_keyboard(self):
        expected_keyboard_commands = [[commands_map['deactivate'], commands_map['status']],
                                      [commands_map['activity_list']]]
        user = User.create(telegram_user_id=0)
        self._check_keyboard_expectations(keyboard_for_user(user).keyboard, expected_keyboard_commands)

    def test_keyboard_rights_level_1(self):
        expected_keyboard_commands = [[commands_map['deactivate'], commands_map['status'], commands_map['summon']],
                                      [commands_map['activity_list']]]
        user = User.create(telegram_user_id=0, rights_level=1)
        self._check_keyboard_expectations(keyboard_for_user(user).keyboard, expected_keyboard_commands)

    def test_superuser_keyboard(self):
        expected_keyboard_commands = [[commands_map['deactivate'], commands_map['status'], commands_map['summon']],
                                      [commands_map['activity_list'], commands_map['moderator_list']]]
        user = User.create(telegram_user_id=0, telegram_login=superuser_login)
        self._check_keyboard_expectations(keyboard_for_user(user).keyboard, expected_keyboard_commands)
