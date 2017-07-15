from unittest import TestCase
from unittest.mock import MagicMock
from app.models import *


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()

        Subscription.delete().execute()
        Participant.delete().execute()
        User.delete().execute()
        Activity.delete().execute()

        self._mm_bot = MagicMock()
        self._mm_update = MagicMock
        self._mm_update.callback_query = None
