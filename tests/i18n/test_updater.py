from unittest import TestCase

from app.core.info import APP_DIR
from app.i18n import updater


class TestStringsUpdater(TestCase):
    def test_default_language(self):
        self.assertIsNotNone(updater.DEFAULT_LANGUAGE)
        self.assertTrue(updater.DEFAULT_LANGUAGE in updater.SUPPORTED_LANGUAGES)

    def test_all_release_strings_are_valid(self):
        instance = updater.TranslationsUpdater(APP_DIR.joinpath('i18n'), APP_DIR)
        self.assertTrue(instance.regenerate_all())
        self.assertTrue(instance.is_translations_generated())
