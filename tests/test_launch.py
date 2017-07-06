from app.zordon import ZordonBot
from telegram.ext import Updater
from unittest import TestCase
from unittest.mock import create_autospec, patch


class TestLaunch(TestCase):
    def test_basic_launch(self):
        telegram_updater_mock = create_autospec(Updater)
        with patch('Updater') as telegram_updater_mock:
            bot_instance = ZordonBot()
