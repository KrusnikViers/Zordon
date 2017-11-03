import gettext
from telegram import Update

from app.models.user import User
from app.common.i18n import updater


# Should be loaded before using.
_translations = {}


def load_translations():
    global _translations
    if not updater.is_translations_compiled():
        updater.regenerate_translations()
    for language in updater.supported_languages:
        _translations[language] = gettext.translation('zordon', localedir=str(updater.locale_dir), languages=[language])


def get_full_name(locale_code: str) -> str:
    if locale_code == 'auto':
        return _('lang_auto')
    elif locale_code == 'ru':
        return 'Русский'
    elif locale_code == 'en':
        return 'English'
    # Should not reach this place.
    assert False


def get(update: Update, user: User):
    if user.locale != 'auto':
        language_code = user.locale
    else:
        language_code = update.effective_user.language_code
        if language_code:
            language_code = language_code.split('-')[0]
    if language_code in _translations:
        return _translations[language_code]
    return _translations['en']
