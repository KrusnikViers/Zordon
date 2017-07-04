import definitions
import telegram.ext as tg_ext
import models

import logging
from logging import info


logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', level=logging.INFO)

updater = tg_ext.Updater(token=definitions.token)
if definitions.is_hook_on:
    updater.start_webhook(listen=definitions.hook_host,
                          port=definitions.hook_port,
                          url_path=definitions.hook_path)
    info('Web hook was enabled, listening')
else:
    updater.start_polling()
    info('Web hook was disabled, polling')

info(updater.bot.get_me())
