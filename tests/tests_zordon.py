from telegram.ext import Updater, Dispatcher
from unittest import TestCase
from unittest.mock import create_autospec, patch, Mock, MagicMock


class UpdaterMock(Updater):
    """ Special class for testing without actual telegram.ext.Updater """
    dispatcher = Dispatcher

updater_mock = create_autospec(UpdaterMock)
with patch('telegram.ext.Updater', new=updater_mock):
    import app.zordon


class TestLaunch(TestCase):
    def setUp(self):
        updater_mock.reset_mock()

    def test_launch(self):
        app.zordon.ZordonBot()
        updater_mock().start_polling.assert_called_once_with()
        assert updater_mock().dispatcher.add_handler.called
