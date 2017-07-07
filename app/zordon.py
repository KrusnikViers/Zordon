from telegram.ext import Updater
import logging
from .definitions import telegram_token
from .commands import set_handlers


class ZordonBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s -- %(message)s', level=logging.INFO)

        self.updater = Updater(token=telegram_token)
        self.updater.start_polling()
        set_handlers(self.updater.dispatcher)
