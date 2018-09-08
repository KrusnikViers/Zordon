from pathlib import Path
from unittest import TestCase
import logging
import os


TEST_DATA_DIR = Path(os.path.realpath(__file__)).parent.joinpath('data')


class MatcherAny:
    def __eq__(self, _):
        return True


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        logging.basicConfig(level=logging.CRITICAL)
