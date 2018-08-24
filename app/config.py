import argparse
import json
import logging
import os
from pathlib import Path
from urllib.parse import urlparse

# Variables below must be initialised at the very start and should not be changed any further.
APP_DIRECTORY = Path(os.path.realpath(__file__)).parent
TELEGRAM_BOT_TOKEN = None
WEBHOOK_URL = None
WEBHOOK_PORT = None

_args = None
_json_configuration = None


def load_user_configuration():
    global TELEGRAM_BOT_TOKEN
    global WEBHOOK_URL
    global WEBHOOK_PORT

    _set_args_and_configuration_file()

    TELEGRAM_BOT_TOKEN = _maybe_get_value('telegram_bot_token')
    WEBHOOK_URL, WEBHOOK_PORT = _parse_webhook_url(_maybe_get_value('webhook_url'))

    _clean_args_and_configuration_file()


def _get_command_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Telegram bot to gather people together.')
    parser.add_argument('--configuration-file', '-c', type=str, default='configuration.json', dest='configuration_file',
                        help='Json-formatted file with all configuration parameters.')
    parser.add_argument('--telegram-bot-token', '-t', type=str, dest='telegram_bot_token',
                        help='Telegram bot token, received from @BotFather.')
    parser.add_argument('--webhook-url', '-w', type=str, dest='webhook_url',
                        help='Webhook URL, forces hook mode if provided.')
    return parser.parse_args()


def _get_config_file_content(file_location: str) -> dict:
    file_location_path = Path(file_location)
    if file_location_path.is_file():
        with file_location_path.open() as configuration_file:
            return json.load(configuration_file)
    logging.info('Configuration file is missing, using only command line parameters.')
    return {}


def _set_args_and_configuration_file():
    global _args
    global _json_configuration
    _args = _get_command_line_arguments()
    _json_configuration = _get_config_file_content(_args.configuration_file)


def _clean_args_and_configuration_file():
    global _args
    global _json_configuration
    del _args
    del _json_configuration


def _maybe_get_value(option_name: str):
    global _args
    global _json_configuration
    value = getattr(_args, option_name)
    return value if value else _json_configuration.get(option_name, None)


def _parse_webhook_url(url)->(str, int):
    if not url:
        return None, None
    port_from_url = urlparse(url).port
    return url, port_from_url if port_from_url else 80
