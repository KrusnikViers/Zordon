from telegram.ext import Updater, Dispatcher
from unittest.mock import create_autospec, patch

from tests.base_test import BaseTestCase


class UpdaterMock(Updater):
    """ Special class for testing without actual telegram.ext.Updater """
    dispatcher = Dispatcher

updater_mock = create_autospec(UpdaterMock)
with patch('telegram.ext.Updater', new=updater_mock):
    import app.zordon


class TestLaunch(BaseTestCase):
    def setUp(self):
        super(TestLaunch, self).setUp()
        updater_mock.reset_mock()

    def test_launch(self):
        app.zordon.ZordonBot()
        updater_mock().start_polling.assert_called_once_with()
        self.assertTrue(updater_mock().dispatcher.add_handler.called)
