from unittest.mock import MagicMock, patch

from app.core import commands
from app.models.all import *
from app.settings import credentials
from tests.base_test import BaseTestCase


updater_mock = MagicMock()
with patch('telegram.ext.Updater', new=updater_mock):
    import app.zordon


class TestLaunch(BaseTestCase):
    def test_launch(self):
        zordon_bot = app.zordon.ZordonBot()
        zordon_bot.run()
        updater_mock().start_polling.assert_called_once_with()

    def test_superuser_auto_update(self):
        users = [
            (0, 'fake_su', commands.superuser_rights_level, 0),
            (1, 'also_fake_su', commands.superuser_rights_level, 0),
            (2, 'basic_user', 0, 0),
            (3, 'advanced_user', 1, 1),
            (4, credentials.superuser, 1, commands.superuser_rights_level),
        ]

        for tg_id, login, rights, _ in users:
            User.create(telegram_id=tg_id, login=login, rights=rights)
        self.assertEqual(len(users), User.select().count())

        zordon_bot = app.zordon.ZordonBot()
        zordon_bot.run()

        for tg_id, login, _, new_rights in users:
            self.assertTrue(User.select().where((User.telegram_id == tg_id) &
                                                (User.login == login) &
                                                (User.rights == new_rights)).exists())
        self.assertEqual(len(users), User.select().count())
