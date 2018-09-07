from datetime import datetime
import os
import alembic.config

from app.core.info import APP_DIR
from app.database.migrations.engine import ScopedEngine


def _in_database_dir(command):
    def impl(*args, **kwargs):
        initial_cwd = os.getcwd()
        os.chdir(APP_DIR.joinpath('database'))
        command(*args, **kwargs)
        os.chdir(initial_cwd)
    return impl


@_in_database_dir
def run_migrations(engine):
    with ScopedEngine(engine):
        alembic.config.main(argv=['upgrade', 'head'])


@_in_database_dir
def make_migrations(engine):
    message = 'auto_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    with ScopedEngine(engine):
        alembic.config.main(argv=['revision', '--autogenerate', '-m', message])
