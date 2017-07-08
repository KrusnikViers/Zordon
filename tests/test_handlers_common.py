from unittest import TestCase
from app.models import *
from app.handlers.common import commands_map, keyboard_for_user
from app.definitions import superuser_login


class TestModels(TestCase):
    def setUp(self):
        User.delete().execute()

    def test_inactive_user_keyboard(self):
        expected_keyboard_commands = [commands_map['activate'], commands_map['status'], commands_map['activity_list']]
        user = User.create(telegram_user_id=0, telegram_chat_id=0, is_active=False)
        keyboard = keyboard_for_user(user).keyboard[0]

        self.assertEqual(len(keyboard), len(expected_keyboard_commands))
        for i in range(0, len(keyboard)):
            self.assertEqual(keyboard[i].text, '/' + expected_keyboard_commands[i])

    def test_usual_user_keyboard(self):
        expected_keyboard_commands = [commands_map['deactivate'], commands_map['status'], commands_map['activity_list']]
        user = User.create(telegram_user_id=0, telegram_chat_id=0)
        keyboard = keyboard_for_user(user).keyboard[0]

        self.assertEqual(len(keyboard), len(expected_keyboard_commands))
        for i in range(0, len(keyboard)):
            self.assertEqual(keyboard[i].text, '/' + expected_keyboard_commands[i])

    def test_keyboard_rights_level_1(self):
        expected_keyboard_commands = [commands_map['deactivate'], commands_map['status'], commands_map['summon'],
                                      commands_map['activity_list']]
        user = User.create(telegram_user_id=0, telegram_chat_id=0, rights_level=1)
        keyboard = keyboard_for_user(user).keyboard[0]

        self.assertEqual(len(keyboard), len(expected_keyboard_commands))
        for i in range(0, len(keyboard)):
            self.assertEqual(keyboard[i].text, '/' + expected_keyboard_commands[i])

    def test_superuser_keyboard(self):
        expected_keyboard_commands = [commands_map['deactivate'], commands_map['status'], commands_map['summon'],
                                      commands_map['activity_list'], commands_map['moderator_list']]
        user = User.create(telegram_user_id=0, telegram_chat_id=0, telegram_login='@' + superuser_login)
        keyboard = keyboard_for_user(user).keyboard[0]

        self.assertEqual(len(keyboard), len(expected_keyboard_commands))
        for i in range(0, len(keyboard)):
            self.assertEqual(keyboard[i].text, '/' + expected_keyboard_commands[i])
