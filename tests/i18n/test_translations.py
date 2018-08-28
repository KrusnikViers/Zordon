from unittest import TestCase, mock

from app.i18n.translations import TranslationsList


class TestTranslations(TestCase):
    def test_get_no_language_code(self):
        TranslationsList.initialise()
        update_mock = mock.MagicMock()
        update_mock.effective_user.language_code = None
        self.assertEqual(TranslationsList.translations['en'], TranslationsList.get_for_update(update_mock))

    def test_get_correct_code(self):
        TranslationsList.initialise()
        update_mock = mock.MagicMock()
        update_mock.effective_user.language_code = 'ru-Ru'
        self.assertEqual(TranslationsList.translations['ru'], TranslationsList.get_for_update(update_mock))

    def test_get_fallback(self):
        TranslationsList.initialise()
        update_mock = mock.MagicMock()
        update_mock.effective_user.language_code = 'un-Known'
        self.assertEqual(TranslationsList.translations['en'], TranslationsList.get_for_update(update_mock))
