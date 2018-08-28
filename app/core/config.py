import argparse
import dj_database_url
import json
import logging
import os
import pathlib
import urllib.parse


APP_DIRECTORY = pathlib.Path(os.path.realpath(__file__)).parent.parent
TELEGRAM_BOT_TOKEN = None
WEBHOOK_URL = None
WEBHOOK_PORT = None
DATABASE_CREDENTIALS = None


def load_user_configuration():
    global TELEGRAM_BOT_TOKEN
    global WEBHOOK_URL
    global WEBHOOK_PORT
    global DATABASE_CREDENTIALS

    reader = ConfigurationReader()

    TELEGRAM_BOT_TOKEN = reader.maybe_get_value('telegram_bot_token')
    WEBHOOK_URL, WEBHOOK_PORT = reader.parse_webhook_params(reader.maybe_get_value('webhook_url'))
    DATABASE_CREDENTIALS = reader.parse_database_credentials(reader.maybe_get_value('database_url'))


class ConfigurationReader:
    def __init__(self):
        self.args = self._get_command_line_arguments()
        self.json = self._get_configuration_file_content()

    @staticmethod
    def _get_command_line_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Telegram bot to gather people together.')
        parser.add_argument('--configuration-file', '-c', type=str, default='configuration.json', dest='configuration_file',
                            help='Json-formatted file with all configuration parameters.')
        parser.add_argument('--telegram-bot-token', '-t', type=str, dest='telegram_bot_token',
                            help='Telegram bot token, received from @BotFather.')
        parser.add_argument('--webhook-url', '-w', type=str, dest='webhook_url',
                            help='Webhook URL, forces hook mode if provided.')
        parser.add_argument('--database-url', '-d', type=str, dest='database_url',
                            help='Database url (user:password@host:port/database_name)')
        return parser.parse_args()

    def _get_configuration_file_content(self) -> dict:
        file_location_path = pathlib.Path(self.args.configuration_file)
        if file_location_path.is_file():
            with file_location_path.open() as configuration_file:
                return json.load(configuration_file)
        logging.info('Configuration file is missing, using only command line parameters.')
        return {}

    def maybe_get_value(self, option_name: str):
        value = getattr(self.args, option_name)
        return value if value else self.json.get(option_name, None)

    @staticmethod
    def parse_webhook_params(raw_url) -> (str, int):
        if not raw_url:
            return None, None
        port_from_url = urllib.parse.urlparse(raw_url).port
        return raw_url, port_from_url if port_from_url else 80

    @staticmethod
    def parse_database_credentials(raw_url) -> dict:
        if not raw_url:
            return {}

        schema_delimiter = '://'
        schema_end_index = raw_url.find(schema_delimiter)
        if schema_end_index != -1:
            raw_url = raw_url[schema_end_index + len(schema_delimiter):]

        parsed_url = dj_database_url.parse('postgres://' + raw_url)
        return {
            'database': parsed_url['NAME'],
            'host': parsed_url['HOST'],
            'port': parsed_url['PORT'],
            'user': parsed_url['USER'],
            'password': parsed_url['PASSWORD']
        }
