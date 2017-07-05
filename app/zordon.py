from telegram.ext import Updater
import logging
import definitions
import models
import commands


logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s -- %(message)s', level=logging.INFO)

updater = Updater(token=definitions.telegram_token)
if definitions.is_web_hook_mode:
    updater.start_webhook(listen=definitions.web_hook_params.hostname,
                          port=definitions.web_hook_params.port,
                          url_path=definitions.web_hook_params.path)
else:
    updater.start_polling()

commands.set_handlers(updater.dispatcher)
print(updater.bot.get_me())
