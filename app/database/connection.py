import logging

from flexiconf import Configuration
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.info import DEFAULT_DB_PATH
from app.database.migrations import router


class DatabaseConnection:
    def __init__(self, configuration: Configuration, for_tests: bool = False):
        url = 'sqlite://' if for_tests else 'sqlite:///{}/storage.db'.format(
            configuration.get_string('db_path', default=DEFAULT_DB_PATH))
        self.engine = create_engine(url)
        self.make_session = sessionmaker(bind=self.engine)
        self.run_migrations()

    def run_migrations(self):
        logging.info('Running pending migrations')
        router.run_migrations(self.engine)
