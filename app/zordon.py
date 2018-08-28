import logging
from telegram.ext import Updater

from app.i18n.translations import TranslationsList
from app.core import database, config, dispatcher


class ZordonBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', level=logging.INFO)
        self.updater = None

    # Launch and wait for worker threads, that should be stopped with signals SIGINT(2), SIGTERM(15) or SIGABRT(6).
    def run(self):
        self._set_up()

        logging.info('Launching bot: ' + str(self.updater.bot.get_me()))
        if config.WEBHOOK_URL and config.WEBHOOK_PORT:
            logging.info('Webhook mode via {} on {} port.'.format(config.WEBHOOK_URL, config.WEBHOOK_PORT))
            self.updater.start_webhook(port=config.WEBHOOK_PORT, webhook_url=config.WEBHOOK_URL)
        else:
            logging.info('Polling mode; Webhook information was not provided.')
            self.updater.start_polling()

        # Locking current execution stream.
        self.updater.idle()
        logging.info('Bot finished.')

    def _set_up(self):
        config.load_user_configuration()
        TranslationsList.initialise()
        database.BaseModel.connect_and_migrate(config.DATABASE_CREDENTIALS)
        self.updater = Updater(token=config.TELEGRAM_BOT_TOKEN)
        dispatcher.set_handlers(self.updater.dispatcher)
