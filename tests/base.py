from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock
import logging
import os

from app.core.configuration import Configuration
from app.database.connection import DatabaseConnection
from app.database.scoped_session import ScopedSession
from app.models.all import Group, Response, Request, User


class MatcherAny:
    def __eq__(self, _):
        return True


def mock_effective_user(update, tg_id, username, full_name):
    type(update.effective_user).id = PropertyMock(return_value=tg_id)
    type(update.effective_user).full_name = PropertyMock(return_value=full_name)
    type(update.effective_user).username = PropertyMock(return_value=username)


def mock_effective_chat(update, tg_id, title):
    type(update.effective_user).id = PropertyMock(return_value=tg_id)
    type(update.effective_user).title = PropertyMock(return_value=title)


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

    def setUp(self):
        super(DatabaseTestCase, self).setUp()
        with ScopedSession(self.connection) as session:
            session.query(User).delete()
            session.query(Response).delete()
            session.query(Request).delete()
            session.query(Group).delete()
