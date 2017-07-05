from telegram.ext import Updater
import definitions
import models


updater = Updater(token=definitions.telegram_token)
if definitions.is_web_hook_mode:
    updater.start_webhook(listen=definitions.web_hook_params.hostname,
                          port=definitions.web_hook_params.port,
                          url_path=definitions.web_hook_params.path)
else:
    updater.start_polling()
