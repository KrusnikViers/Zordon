from telegram.ext import Updater
import logging

from app import definitions
from app.commands import set_handlers


class ZordonBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s -- %(message)s', level=logging.INFO)
        self.updater = Updater(token=definitions.telegram_token)
        set_handlers(self.updater.dispatcher)

    # Run background working threads and wait until they finished.
    # Worker threads will be stopped on signals SIGINT(2), SIGTERM(15) or SIGABRT(6).
    def run(self):
        logging.info('Launching bot: ' + str(self.updater.bot.get_me()))
        self.updater.start_polling()
        self.updater.idle()
        logging.info('Bot finished.')
