import logging

from telegram.ext import Updater

from app.core.configuration import Configuration
from app.core.info import APP_DIR
from app.database.connection import DatabaseConnection
from app.handlers.dispatcher import Dispatcher
from app.i18n.translations import Translations


class Bot:
    def __init__(self):
        self.updater: Updater = None
        self.configuration: Configuration = None
        self.db: DatabaseConnection = None
        self.translations: Translations = None

    def run(self):
        self._set_up()
        logging.info('Launching bot: ' + str(self.updater.bot.get_me()))
        self._start_updater()
        # This call will lock execution until worker threads are stopped with SIGINT(2), SIGTERM(15) or SIGABRT(6).
        self.updater.idle()

    def _start_updater(self):
        if self.configuration.webhook_url:
            logging.info('Webhook mode on {}.'.format(self.configuration.webhook_url))
            self.updater.start_webhook(webhook_url=self.configuration.webhook_url)
        else:
            logging.info('Polling mode; Webhook information was not provided.')
            self.updater.start_polling()

    def _set_up(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', level=logging.INFO)
        self.configuration = Configuration.load()
        self.db = DatabaseConnection(self.configuration)
        self.translations = Translations(APP_DIR.joinpath('i18n'), APP_DIR)
        self.updater = Updater(token=self.configuration.telegram_bot_token,
                               request_kwargs=self.configuration.proxy_params)
        self.dispatcher = Dispatcher(self.configuration, self.updater, self.db, self.translations)
