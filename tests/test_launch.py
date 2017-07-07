from telegram.ext import Updater
from unittest import TestCase
from unittest.mock import create_autospec, patch

_updater_mock = create_autospec(Updater)


class TestLaunch(TestCase):
    def test_basic_launch(self):
        with patch('telegram.ext.Updater') as _updater_mock:
            from app.zordon import ZordonBot
            bot_instance = ZordonBot()
