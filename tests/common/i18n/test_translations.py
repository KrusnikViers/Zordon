import os

from app.common.i18n import translations, updater
from tests.base_test import BaseTestCase


class TestTranslations(BaseTestCase):
    def test_translations_valid(self):
        self.assertTrue(updater.regenerate_translations())

    def test_translations_regenerating(self):
        for lang in updater.supported_languages:
            os.remove(str(updater.locale_dir.joinpath(lang, 'LC_MESSAGES', 'zordon.mo')))
        self.assertFalse(updater.is_translations_compiled())
        updater.regenerate_translations()
        self.assertTrue(updater.is_translations_compiled())

    def test_translations_loading(self):
        for lang in updater.supported_languages:
            os.remove(str(updater.locale_dir.joinpath(lang, 'LC_MESSAGES', 'zordon.mo')))
        self.assertFalse(updater.is_translations_compiled())
        translations.load_translations()
        self.assertTrue(updater.is_translations_compiled())
