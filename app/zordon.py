import logging
from telegram.ext import Updater

from app.settings import credentials, verbosity


class ZordonBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s -- %(message)s', level=verbosity.level)
        self.updater = Updater(token=credentials.token)

    # Run background working threads and wait until they finished.
    # Worker threads will be stopped on signals SIGINT(2), SIGTERM(15) or SIGABRT(6).
    def run(self):
        logging.info('Launching bot: ' + str(self.updater.bot.get_me()))
        self.set_up_on_start()
        self.updater.start_polling()
        self.updater.idle()
        logging.info('Bot stopped working.')

    # Actions, executed every time when bot is restarted.
    def set_up_on_start(self):
        pass
