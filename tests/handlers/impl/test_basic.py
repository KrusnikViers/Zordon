from unittest.mock import MagicMock, PropertyMock

from tests.base import InBotTestCase, ScopedSession
from app.handlers.impl import basic


class TestBasicHandlers(InBotTestCase):
    def test_help_or_start_private(self):
        context = MagicMock()
        type(context).group = PropertyMock(return_value=None)
        basic.on_help_or_start(context)
        context.send_response_message.assert_called_once_with('Zordon v3.0.0_help_for_private')

    def test_help_or_start_group(self):
        context = MagicMock()
        basic.on_help_or_start(context)
        context.send_response_message.assert_called_once_with('Zordon v3.0.0_help_for_group')

    def test_click_here(self):
        context = MagicMock()
        basic.on_click_here(context)
        context.send_response_message.assert_called_once_with(_('rdr2_easter_egg'))
