from app import config
from app.database import connection, updater


config.load_user_configuration()
connection.initialise()

# First, flush pending migrations, if any.
updater.run_migrations()
updater.make_migrations()
