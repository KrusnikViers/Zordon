import builtins
import logging
import os
from unittest import TestCase

from app.core.configuration import Configuration
from app.database.connection import DatabaseConnection
from app.database.scoped_session import ScopedSession
from app.models.all import Group, Request, Response, User


class MatcherAny:
    def __eq__(self, _):
        return True


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        logging.disable(logging.INFO)
        logging.disable(logging.WARNING)
        logging.disable(logging.ERROR)


class InBotTestCase(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(InBotTestCase, self).__init__(*args, **kwargs)

        self.configuration = Configuration.load()
        if 'CI_DATABASE' in os.environ:
            self.configuration.database_url = Configuration._parse_database_url(os.environ['CI_DATABASE'])
        self.connection = DatabaseConnection(self.configuration)

    def setUp(self):
        super(InBotTestCase, self).setUp()
        with ScopedSession(self.connection) as session:
            session.query(User).delete()
            session.query(Response).delete()
            session.query(Request).delete()
            session.query(Group).delete()

        # Mock translation function, so that localized strings will be returned as their identifiers.
        # This will be overriden in real translation setup, if needed.
        if not getattr(builtins, '_', None):
            builtins._ = lambda x: x
