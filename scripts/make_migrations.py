from app.core.configuration import Configuration
from app.database.connection import DatabaseConnection
from app.database.migrations import router

configuration = Configuration.load()
connection = DatabaseConnection(configuration)

router.make_migrations(connection.engine)
