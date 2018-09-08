from unittest import TestCase
import logging
import os

from app.core.configuration import Configuration
from app.database.connection import DatabaseConnection


class MatcherAny:
    def __eq__(self, _):
        return True


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        logging.disable(logging.INFO)
        logging.disable(logging.WARNING)
        logging.disable(logging.ERROR)


class DatabaseTestCase(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(DatabaseTestCase, self).__init__(*args, **kwargs)

        self.configuration = Configuration.load()
        if 'CI_DATABASE' in os.environ:
            self.configuration.database_url = Configuration.parse_database_url(os.environ['CI_DATABASE'])
        self.connection = DatabaseConnection(self.configuration)
