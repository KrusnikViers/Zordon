import logging

from tests.base import DatabaseTestCase


class TestMigrations(DatabaseTestCase):
    def test_connection(self):
        self.assertIsNotNone(self.connection.engine)
        with self.connection.engine.connect():
            pass