import os
from pathlib import Path
from unittest.mock import patch

from app.core.configuration import Configuration
from tests.base import BaseTestCase


class TestConfig(BaseTestCase):
    test_configuration = Path(os.path.realpath(__file__)).parent.joinpath('data', 'configuration.json')

    @patch('sys.argv', ['_', '-t', 'test_token', '-w', 'http://test_webhook.url:999','-d', 'a:b@c.d:1/e',
                             '-s', 'test_user',
                             '-p', 'socks5://test.com:1', '-pu', 'proxy_user', '-pp', 'proxy_password'])
    def test_command_line(self):
        config = Configuration.load()
        self.assertEqual('test_token', config.telegram_bot_token)
        self.assertEqual('http://test_webhook.url:999', config.webhook_url)
        self.assertEqual('postgresql+psycopg2://a:b@c.d:1/e', config.database_url)
        self.assertEqual('@test_user', config.superuser_login)
        self.assertEqual('socks5://test.com:1', config.proxy_params['proxy_url'])
        self.assertEqual('proxy_user', config.proxy_params['urllib3_proxy_kwargs']['username'])
        self.assertEqual('proxy_password', config.proxy_params['urllib3_proxy_kwargs']['password'])

    @patch('sys.argv', ['_', '-c', str(test_configuration)])
    def test_read_from_file(self):
        config = Configuration.load()
        self.assertEqual('bot_token:for_test', config.telegram_bot_token)
        self.assertEqual('http://zordon.bot:11', config.webhook_url)
        self.assertEqual('postgresql+psycopg2://json:database@test.com:111/db_name', config.database_url)
        self.assertEqual('@viers_test', config.superuser_login)
        self.assertEqual('socks5://test.com', config.proxy_params['proxy_url'])
        self.assertEqual('socks5_user', config.proxy_params['urllib3_proxy_kwargs']['username'])
        self.assertEqual('socks5_password', config.proxy_params['urllib3_proxy_kwargs']['password'])

    @patch('sys.argv', ['_', '-c', str(test_configuration), '-t', 'token_override'])
    def test_command_line_priority(self):
        config = Configuration.load()
        self.assertEqual('token_override', config.telegram_bot_token)
        self.assertEqual('http://zordon.bot:11', config.webhook_url)
