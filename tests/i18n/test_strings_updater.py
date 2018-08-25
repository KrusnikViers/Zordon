from unittest import TestCase

from app.i18n import strings_updater


class TestStringsUpdater(TestCase):
    def test_all_strings_are_valid(self):
        self.assertTrue(strings_updater.regenerate_translations())
        self.assertTrue(strings_updater.is_translations_generated())
