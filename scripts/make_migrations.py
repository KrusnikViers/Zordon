from app.core.configuration import Configuration
from app.database.connection import DatabaseConnection
from app.database.migrations import router

configuration = Configuration.load()
connection = DatabaseConnection(configuration)

# First, flush pending migrations, if any.
connection.run_migrations()

router.make_migrations(connection.engine)
