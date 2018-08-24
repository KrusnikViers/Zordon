import gettext
from telegram import Update

from app.i18n import strings_updater


_translations = {}


def initialise():
    global _translations
    if not strings_updater.is_translations_generated():
        strings_updater.regenerate_translations()
    for language in strings_updater.SUPPORTED_LANGUAGES:
        _translations[language] = gettext.translation('zordon',
                                                      localedir=str(strings_updater.LOCALE_DIR),
                                                      languages=[language])


def get(update: Update):
    language_code = update.effective_user.language_code
    if language_code:
        language_code = language_code.split('-')[0]
    if language_code in _translations:
        return _translations[language_code]
    return _translations['en']
