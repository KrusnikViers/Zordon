from telegram import Bot, Update

from app.i18n import translations


def translatable_handler(handler):
    def wrapper(bot: Bot, update: Update):
        translations.get(update).install()
        handler(bot, update)
    return wrapper
