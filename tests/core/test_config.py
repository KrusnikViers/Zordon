from unittest.mock import patch
from unittest import TestCase

from app.core import config
from tests.base import TEST_DATA_DIR


class TestConfig(TestCase):
    @patch('sys.argv', ['_', '-t', 'test_value_token', '-w', 'http://test_webhook.url:999', '-d', 'a:b@c.d:1/e'])
    def test_command_line(self):
        config.load_user_configuration()
        self.assertEqual('test_value_token', config.TELEGRAM_BOT_TOKEN)
        self.assertEqual('http://test_webhook.url:999', config.WEBHOOK_URL)
        self.assertEqual(999, config.WEBHOOK_PORT)
        self.assertEqual({'database': 'e', 'host': 'c.d', 'port': 1, 'user': 'a', 'password': 'b'},
                         config.DATABASE_CREDENTIALS)

    @patch('sys.argv', ['_', '-c', str(TEST_DATA_DIR.joinpath('example_configuration.json'))])
    def test_read_from_file(self):
        config.load_user_configuration()
        self.assertEqual('bot_token:for_test', config.TELEGRAM_BOT_TOKEN)
        self.assertEqual('http://zordon.bot:11', config.WEBHOOK_URL)
        self.assertEqual(11, config.WEBHOOK_PORT)
        self.assertEqual(
            {'database': 'db_name', 'host': 'test.com', 'port': 111, 'user': 'json', 'password': 'database'},
            config.DATABASE_CREDENTIALS)

    @patch('sys.argv', ['_', '-c', str(TEST_DATA_DIR.joinpath('example_configuration.json')), '-t', 'token_override'])
    def test_command_line_priority(self):
        config.load_user_configuration()
        self.assertEqual('token_override', config.TELEGRAM_BOT_TOKEN)
        self.assertEqual('http://zordon.bot:11', config.WEBHOOK_URL)
        self.assertEqual(11, config.WEBHOOK_PORT)
