import gettext
import pathlib
from telegram import Update
import os

from app.models.user import User


_ru = gettext.translation('common', localedir=str(pathlib.Path(os.path.realpath(__file__)).parent), languages=['ru'])
_en = gettext.translation('common', localedir=str(pathlib.Path(os.path.realpath(__file__)).parent), languages=['en'])


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
    language_code = update.effective_user.language_code
    if language_code:
        language_code = language_code.split('-')[0]

    if language_code == 'ru':
        return _ru
    return _en
