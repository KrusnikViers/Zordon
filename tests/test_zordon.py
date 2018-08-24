from unittest.mock import MagicMock, patch
from unittest import TestCase

updater_mock = MagicMock()
with patch('telegram.ext.Updater', new=updater_mock):
    import app.zordon


class TestLaunch(TestCase):
    def test_polling(self):
        zordon_bot = app.zordon.ZordonBot()
        zordon_bot.run()
        updater_mock().start_polling.assert_called_once_with()
        self.assertTrue(updater_mock().dispatcher.add_handler.called)

