from unittest import TestCase
from app.models import *
from app.handlers.common import commands_map
from app.definitions import superuser_login


class TestModels(TestCase):
    def setUp(self):
        User.delete().execute()

    def test_usual_user_rights(self):
        allowed_commands = {'start', 'status', 'activate', 'deactivate', 'activity_list', 'subscribe', 'unsubscribe',
                            'join', 'later', 'decline'}
        user = User.create(telegram_user_id=0, telegram_chat_id=0)
        for command in commands_map:
            self.assertEqual(user.has_right(command), (command in allowed_commands))

    def test_rights_level_1(self):
        allowed_commands = {'start', 'status', 'activate', 'deactivate', 'activity_list', 'activity_add', 'subscribe',
                            'unsubscribe', 'summon', 'join', 'later', 'decline'}
        user = User.create(telegram_user_id=0, telegram_chat_id=0, rights_level=1)
        for command in commands_map:
            self.assertEqual(user.has_right(command), (command in allowed_commands))

    def test_superuser_rights(self):
        user = User.create(telegram_user_id=0, telegram_chat_id=0, telegram_login='@' + superuser_login)
        for command in commands_map:
            self.assertTrue(user.has_right(command))
