from telegram.ext import Updater
import logging

from app.base import settings
from app.commands import set_handlers


class ZordonBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s -- %(message)s', level=settings.verbosity)
        self.updater = Updater(token=settings.token)

    # Run background working threads and wait until they finished.
    # Worker threads will be stopped on signals SIGINT(2), SIGTERM(15) or SIGABRT(6).
    def run(self):
        logging.info('Launching bot: ' + str(self.updater.bot.get_me()))
        self.updater.start_polling()
        self.updater.idle()
        logging.info('Bot finished.')
