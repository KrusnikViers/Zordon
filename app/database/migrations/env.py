from alembic import context

from app.database.migrations.engine import get_scoped_engine

# This forces all models to be defined, and therefore to be added in the Base model metadata.
from app.database.model import Base
from app.models.all import *


target_metadata = Base.metadata
with get_scoped_engine().connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
