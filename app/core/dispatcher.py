import logging
from telegram.ext import Dispatcher

from app.core.utility import report
from app.core.handlers import user


def attach_all_handlers(dispatcher: Dispatcher):
    def attach_handlers(handlers: list, module_name: str):
        logging.info('Registering {0} handlers from {1} module...'.format(len(handlers), module_name))
        for h in handlers:
            dispatcher.add_handler(h)

    attach_handlers(user.get_handlers(), 'user')

    dispatcher.add_error_handler(report.error_handler)
    logging.info('Handlers registered total: {}'.format(len(dispatcher.handlers[0])))
