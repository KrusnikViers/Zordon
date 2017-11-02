from unittest import mock, TestCase

from app.models.all import *


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()

        ActivityAccess.delete().execute()
        Activity.delete().execute()
        Subscription.delete().execute()
        User.delete().execute()

        self._mm_bot = mock.MagicMock()
        self._mm_update = mock.MagicMock
        self._mm_update.callback_query = None
        self._mm_update.message = None

    class Any:
        def __eq__(self, other):
            return True
