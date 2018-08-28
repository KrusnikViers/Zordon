from unittest.mock import MagicMock, patch
from unittest import TestCase

import app.zordon
import app.core.database

from tests.base import MatcherAny


class TestLaunch(TestCase):
    @patch('app.zordon.Updater', new=MagicMock())
    @patch('app.zordon.database', new=MagicMock())
    def test_polling(self):
        zordon_bot = app.zordon.ZordonBot()
        zordon_bot.run()

        zordon_bot.updater.start_polling.assert_called_once_with()
        zordon_bot.updater.dispatcher.add_handler.assert_called_with(MatcherAny())
        self.assertFalse(zordon_bot.updater.start_webhook.called)
        self.assertTrue(app.zordon.database.initialise.called)

    @patch('app.zordon.Updater', new=MagicMock())
    @patch('app.zordon.database', new=MagicMock())
    @patch('sys.argv', ['_', '-w', 'http://test.url:1199'])
    def test_webhook(self):
        zordon_bot = app.zordon.ZordonBot()
        zordon_bot.run()

        zordon_bot.updater.start_webhook.assert_called_once_with(webhook_url='http://test.url:1199', port=1199)
        zordon_bot.updater.dispatcher.add_handler.assert_called_with(MatcherAny())
        self.assertFalse(zordon_bot.updater.start_polling.called)
        self.assertTrue(app.zordon.database.initialise.called)

