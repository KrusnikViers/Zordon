import gettext
import logging
from telegram import Update

from app.i18n.updater import TranslationsUpdater, SUPPORTED_LANGUAGES
from app import config


_translations = {}


def initialise():
    global _translations
    updater = TranslationsUpdater()
    if not updater.is_translations_generated():
        logging.info('Precompiled translations not found, regenerating...')
        updater.regenerate_translations()
    for language in SUPPORTED_LANGUAGES:
        _translations[language] = gettext.translation('zordon',
                                                      localedir=str(config.APP_DIR.joinpath('i18n')),
                                                      languages=[language])


def get_for_update(update: Update):
    language_code = update.effective_user.language_code
    if language_code:
        language_code = language_code.split('-')[0]
    if language_code in SUPPORTED_LANGUAGES:
        return _translations[language_code]
    return _translations['en']
