import gettext
from telegram import Update

from app.i18n.updater import TranslationsUpdater, SUPPORTED_LANGUAGES
from app.core import config


class TranslationsList:
    translations = {}

    @classmethod
    def initialise(cls):
        updater = TranslationsUpdater()
        if not updater.is_translations_generated():
            updater.regenerate_translations()
        for language in SUPPORTED_LANGUAGES:
            cls.translations[language] = gettext.translation('zordon',
                                                             localedir=str(config.APP_DIRECTORY.joinpath('i18n')),
                                                             languages=[language])

    @classmethod
    def get_for_update(cls, update: Update):
        language_code = update.effective_user.language_code
        if language_code:
            language_code = language_code.split('-')[0]
        if language_code in SUPPORTED_LANGUAGES:
            return cls.translations[language_code]
        return cls.translations['en']
