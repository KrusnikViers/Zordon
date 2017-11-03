import logging

from telegram.ext import Updater

from app.common import credentials, verbosity
from app.common.i18n import translations
from app.core import commands, dispatcher
from app.models.all import *


class ZordonBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s|%(levelname)s: %(message)s', level=verbosity.level)
        self.updater = None  # Should be initialized during |set_up_on_start|

    # Run background working threads and wait until they finished.
    # Worker threads will be stopped on signals SIGINT(2), SIGTERM(15) or SIGABRT(6).
    def run(self):
        logging.info('Configuring bot...')
        self._set_up_on_start()
        logging.info('Set up finished: ' + str(self.updater.bot.get_me()))
        logging.info('Launching...')
        self.updater.start_polling()
        self.updater.idle()
        logging.info('Bot stopped working.')

    # Actions, executed every time when bot is restarted.
    def _set_up_on_start(self):
        self.updater = Updater(token=credentials.token)
        dispatcher.attach_all_handlers(self.updater.dispatcher)

        # Update superuser status on users.
        logging.info('Superuser set to ' + credentials.superuser)
        User.update(rights=0).where((User.rights == commands.superuser_rights_level) &
                                    (User.login != credentials.superuser)).execute()
        User.update(rights=commands.superuser_rights_level).where(User.login == credentials.superuser).execute()

        # Update and load translations
        translations.load_translations()
