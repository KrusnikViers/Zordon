from unittest import TestCase

from app.i18n.updater import TranslationsUpdater


class TestStringsUpdater(TestCase):
    def test_all_strings_are_valid(self):
        updater = TranslationsUpdater()
        self.assertTrue(updater.regenerate_translations())
        self.assertTrue(updater.is_translations_generated())
