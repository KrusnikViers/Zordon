import logging

from flexiconf import Configuration
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.migrations import router


class DatabaseConnection:
    def __init__(self, configuration: Configuration):
        url = 'postgresql+psycopg2://' + configuration.get_string('database_url').split('://')[-1]
        self.engine = create_engine(url)
        self.make_session = sessionmaker(bind=self.engine)
        self.run_migrations()

    def run_migrations(self):
        logging.info('Running pending migrations')
        router.run_migrations(self.engine)
