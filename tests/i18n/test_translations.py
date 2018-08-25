from unittest import TestCase, mock

from app.i18n import translations


class TestTranslations(TestCase):
    def test_get_no_language_code(self):
        translations.initialise()
        update_mock = mock.MagicMock()
        update_mock.effective_user.language_code = None
        self.assertEqual(translations._translations['en'], translations.get(update_mock))

    def test_get_correct_code(self):
        translations.initialise()
        update_mock = mock.MagicMock()
        update_mock.effective_user.language_code = 'ru-Ru'
        self.assertEqual(translations._translations['ru'], translations.get(update_mock))

    def test_get_fallback(self):
        translations.initialise()
        update_mock = mock.MagicMock()
        update_mock.effective_user.language_code = 'un-Known'
        self.assertEqual(translations._translations['en'], translations.get(update_mock))
