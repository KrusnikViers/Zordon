from flexiconf import ArgsLoader, Configuration, JsonLoader

from app.core.info import APP_DIR
from app.database.connection import DatabaseConnection
from app.database.migrations import router

bare_args_config = Configuration([ArgsLoader()])
config = Configuration([
    JsonLoader(bare_args_config.get_string('config', default=str(APP_DIR.joinpath('configuration.json')))),
    ArgsLoader()
])

connection = DatabaseConnection(config)

router.make_migrations(connection.engine)
