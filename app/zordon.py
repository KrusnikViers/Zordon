import logging
from logging import info
from telegram.ext import Updater

import definitions
import models


logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=definitions.telegram_token)
if definitions.is_web_hook_mode:
    updater.start_webhook(listen=definitions.web_hook_params.hostname,
                          port=definitions.web_hook_params.port,
                          url_path=definitions.web_hook_params.path)
    info('Web hook is enabled, listening on {0}'.format(definitions.web_hook_params.geturl()))
else:
    updater.start_polling()
    info('Web hook is not set, polling')

info(updater.bot.get_me())
