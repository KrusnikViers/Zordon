import argparse
import json
import logging
import pathlib


class Configuration:
    def __init__(self, _telegram_bot_token, _superuser_login, _webhook_url, _database_url, _proxy_params):
        self.telegram_bot_token: str = _telegram_bot_token
        self.webhook_url: str = _webhook_url
        self.superuser_login: str = _superuser_login
        self.database_url: str = _database_url
        self.proxy_params = _proxy_params

    @classmethod
    def load(cls):
        args = cls._get_command_line_arguments()
        json_config = cls._get_configuration_file_content(args.configuration_file)

        def maybe_get_value(option_name: str):
            value = getattr(args, option_name)
            return value if value else json_config.get(option_name, None)

        return cls(maybe_get_value('telegram_bot_token'),
                   cls._parse_telegram_login(maybe_get_value('superuser')),
                   maybe_get_value('webhook_url'),
                   cls._parse_database_url(maybe_get_value('database_url')),
                   cls._make_proxy_parameters(maybe_get_value('proxy_url'),
                                              maybe_get_value('proxy_user'),
                                              maybe_get_value('proxy_password')))

    @staticmethod
    def _get_command_line_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Telegram bot to gather people together.')
        parser.add_argument('--configuration-file', '-c', type=str, default='configuration.json',
                            dest='configuration_file',
                            help='Json-formatted file with all configuration parameters.')
        parser.add_argument('--telegram-bot-token', '-t', type=str, dest='telegram_bot_token',
                            help='Telegram bot token, received from @BotFather.')
        parser.add_argument('--webhook-url', '-w', type=str, dest='webhook_url',
                            help='Webhook URL, forces hook mode if provided.')
        parser.add_argument('--superuser', '-s', type=str, dest='superuser',
                            help='Telegram login of user to manage bot and receive support messages.')
        parser.add_argument('--database-url', '-d', type=str, dest='database_url',
                            help='Database url (user:password@host:port/database_name)')
        parser.add_argument('--proxy-url', '-p', type=str, dest='proxy_url', help='Socks5 proxy server URL.')
        parser.add_argument('--proxy-user', '-pu', type=str, dest='proxy_user', help='Username for the proxy server.')
        parser.add_argument('--proxy-password', '-pp', type=str, dest='proxy_password',
                            help='Password for the proxy server.')
        return parser.parse_args()

    @staticmethod
    def _parse_telegram_login(raw_login) -> str:
        if raw_login and raw_login[0] != '@':
            return '@' + raw_login
        return raw_login

    @staticmethod
    def _parse_database_url(raw_url) -> str:
        if not raw_url:
            return raw_url
        return 'postgresql+psycopg2://' + raw_url.split('://')[-1]

    @staticmethod
    def _make_proxy_parameters(proxy_url, proxy_user, proxy_password):
        params = None
        if proxy_url:
            params = {'proxy_url': proxy_url, 'urllib3_proxy_kwargs': {}}
            if proxy_user:
                params['urllib3_proxy_kwargs']['username'] = proxy_user
            if proxy_password:
                params['urllib3_proxy_kwargs']['password'] = proxy_password
        return params

    @staticmethod
    def _get_configuration_file_content(configuration_file_path: str) -> dict:
        file_location_path = pathlib.Path(configuration_file_path)
        if file_location_path.is_file():
            with file_location_path.open() as configuration_file:
                return json.load(configuration_file)
        logging.info('Configuration file is missing, using only command line parameters.')
        return {}
