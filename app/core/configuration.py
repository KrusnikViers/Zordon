import argparse
import json
import logging
import pathlib


class Configuration:
    def __init__(self, _telegram_bot_token, _webhook_url, _database_url):
        self.telegram_bot_token: str = _telegram_bot_token
        self.webhook_url: str = _webhook_url
        self.database_url: str = _database_url

    @classmethod
    def load(cls):
        args = cls._get_command_line_arguments()
        json_config = cls._get_configuration_file_content(args.configuration_file)

        def maybe_get_value(option_name: str):
            value = getattr(args, option_name)
            return value if value else json_config.get(option_name, None)

        return cls(maybe_get_value('telegram_bot_token'),
                   maybe_get_value('webhook_url'),
                   cls._parse_database_url(maybe_get_value('database_url')))

    @staticmethod
    def _parse_database_url(raw_url) -> str:
        if not raw_url:
            return raw_url
        return 'postgresql+psycopg2://' + raw_url.split('://')[-1]

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
        parser.add_argument('--database-url', '-d', type=str, dest='database_url',
                            help='Database url (user:password@host:port/database_name)')
        return parser.parse_args()

    @staticmethod
    def _get_configuration_file_content(configuration_file_path: str) -> dict:
        file_location_path = pathlib.Path(configuration_file_path)
        if file_location_path.is_file():
            with file_location_path.open() as configuration_file:
                return json.load(configuration_file)
        logging.info('Configuration file is missing, using only command line parameters.')
        return {}
