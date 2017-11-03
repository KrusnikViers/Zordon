import os

from app.common.i18n import translations, updater
from tests.base_test import BaseTestCase


class TestTranslations(BaseTestCase):
    @staticmethod
    def purge_compiled_translations():
        for lang in updater.supported_languages:
            if updater.locale_dir.joinpath(lang, 'LC_MESSAGES', 'zordon.mo').is_file():
                os.remove(str(updater.locale_dir.joinpath(lang, 'LC_MESSAGES', 'zordon.mo')))

    def test_translations_valid(self):
        self.assertTrue(updater.regenerate_translations())

    def test_translations_regenerating(self):
        self.purge_compiled_translations()
        self.assertFalse(updater.is_translations_compiled())
        updater.regenerate_translations()
        self.assertTrue(updater.is_translations_compiled())

    def test_translations_loading(self):
        self.purge_compiled_translations()
        self.assertFalse(updater.is_translations_compiled())
        translations.load_translations()
        self.assertTrue(updater.is_translations_compiled())
