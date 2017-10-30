from telegram.ext import Updater, Dispatcher
from unittest.mock import create_autospec, patch, MagicMock

from tests.base_test import BaseTestCase


updater_mock = MagicMock()
with patch('telegram.ext.Updater', new=updater_mock):
    import app.zordon


class TestLaunch(BaseTestCase):
    def test_launch(self):
        zordon_bot = app.zordon.ZordonBot()
        zordon_bot.run()
        updater_mock().start_polling.assert_called_once_with()
        self.assertTrue(updater_mock().dispatcher.add_handler.called)
