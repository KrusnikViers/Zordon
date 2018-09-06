import logging
from telegram.ext import Updater

from app import config
from app.database import connection
from app.i18n import translations
from app.handlers import dispatcher


class ZordonBot:
    def __init__(self):
        self.updater = None

    # Launch and wait for worker threads, that should be stopped with signals SIGINT(2), SIGTERM(15) or SIGABRT(6).
    def run(self):
        self._set_up()
        logging.info('Launching bot: ' + str(self.updater.bot.get_me()))
        self.start_updater()

        # This call will lock execution thread until worker threads are done.
        self.updater.idle()

        logging.info('Bot finished.')

    def start_updater(self):
        if config.WEBHOOK_URL and config.WEBHOOK_PORT:
            logging.info('Webhook mode via {} on {}.'.format(config.WEBHOOK_URL, config.WEBHOOK_PORT))
            self.updater.start_webhook(port=config.WEBHOOK_PORT, webhook_url=config.WEBHOOK_URL)
        else:
            logging.info('Polling mode; Webhook information was not provided.')
            self.updater.start_polling()

    def _set_up(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', level=logging.INFO)
        config.load_user_configuration()
        translations.initialise()
        connection.initialise()

        self.updater = Updater(token=config.TELEGRAM_BOT_TOKEN)
        dispatcher.set_handlers(self.updater.dispatcher)
