from flexiconf import ArgsLoader, Configuration, JsonLoader

from app.database.connection import DatabaseConnection
from app.database.migrations import router

# Provide db_path command line parameter for this script.
# Also, make sure that directory app/database/migrations/versions exists!
config = Configuration([ArgsLoader()])
connection = DatabaseConnection(config)

router.make_migrations(connection.engine)
