from unittest import TestCase
import logging


class MatcherAny:
    def __eq__(self, _):
        return True


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        logging.basicConfig(level=logging.CRITICAL)
