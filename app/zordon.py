from telegram.ext import Updater
import logging
import definitions
import commands


class ZordonBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s -- %(message)s', level=logging.INFO)

        self.updater = Updater(token=definitions.telegram_token)
        if definitions.web_hook_params:
            self.updater.start_webhook(listen=definitions.web_hook_params.hostname,
                                  port=definitions.web_hook_params.port,
                                  url_path=definitions.web_hook_params.path)
        else:
            self.updater.start_polling()

        commands.set_handlers(self.updater.dispatcher)
        print(self.updater.bot.get_me())

if __name__ == '__main__':
    instance = ZordonBot()
