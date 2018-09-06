from alembic import context
from logging.config import fileConfig

from app.database import connection as app_connection
from app.database.model import Base

# This forces all models to be defined, and therefore to be added in the Base model metadata.
from app.models.all import *


fileConfig(context.config.config_file_name)
target_metadata = Base.metadata

with app_connection.engine.connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
