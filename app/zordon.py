import logging
from telegram.ext import Updater

from .commands import set_handlers
from .definitions import telegram_token


class ZordonBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s -- %(message)s', level=logging.INFO)

        self.updater = Updater(token=telegram_token)
        self.updater.start_polling()
        set_handlers(self.updater.dispatcher)
