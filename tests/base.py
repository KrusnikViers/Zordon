from unittest import TestCase
from pathlib import Path
import os

from app import config
from app.database import connection

TEST_DATA_DIR = Path(os.path.realpath(__file__)).parent.joinpath('data')


class MatcherAny:
    def __eq__(self, _):
        return True


class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        # In CI systems, database URL can be passed via environment variable.
        if 'CI_DATABASE' in os.environ:
            database_url = config.parse_database_url(os.environ['CI_DATABASE'])
        else:
            config.load_user_configuration()
            database_url = config.DATABASE_URL
        connection.initialise(database_url)
