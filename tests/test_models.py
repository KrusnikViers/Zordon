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
        user = User.create(telegram_id=0, is_active=True, is_moderator=False)
        for command in commands_map:
            self.assertEqual(user.has_right(command), (command in allowed_commands))

    def test_moderator_rights(self):
        allowed_commands = {'start', 'status', 'activate', 'deactivate', 'activity_list', 'activity_add', 'subscribe',
                            'unsubscribe', 'summon', 'join', 'later', 'decline'}
        user = User.create(telegram_id=0, is_active=True, is_moderator=True)
        for command in commands_map:
            self.assertEqual(user.has_right(command), (command in allowed_commands))

    def test_superuser_rights(self):
        user = User.create(telegram_id=0, telegram_login='@' + superuser_login, is_active=True, is_moderator=False)
        for command in commands_map:
            self.assertTrue(user.has_right(command))
