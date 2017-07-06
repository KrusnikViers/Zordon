from telegram.ext import Updater
import logging
from .definitions import telegram_token, web_hook_params
from .commands import set_handlers


class ZordonBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s -- %(message)s', level=logging.INFO)

        self.updater = Updater(token=telegram_token)
        if web_hook_params:
            self.updater.start_webhook(listen=web_hook_params.hostname,
                                       port=web_hook_params.port,
                                       url_path=web_hook_params.path)
        else:
            self.updater.start_polling()

        set_handlers(self.updater.dispatcher)
        print(self.updater.bot.get_me())
