from unittest import TestCase
from pathlib import Path
import os

from app.core import config, database


TEST_DATA_DIR = Path(os.path.realpath(__file__)).parent.joinpath('data')


class MatcherAny:
    def __eq__(self, _):
        return True


class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        # In CI systems, database URL can be passed via environment variable.
        if 'CI_DATABASE' in os.environ:
            credentials = config.ConfigurationReader.parse_database_credentials(os.environ['CI_DATABASE'])
        else:
            config.load_user_configuration()
            credentials = config.DATABASE_CREDENTIALS
        database.BaseModel.connect_and_migrate(credentials)
