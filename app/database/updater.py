from datetime import datetime
import os
import alembic.config

from app.config import APP_DIR


def _in_database_dir(command):
    def impl():
        initial_cwd = os.getcwd()
        os.chdir(APP_DIR.joinpath('database'))
        command()
        os.chdir(initial_cwd)
    return impl


@_in_database_dir
def run_migrations():
    alembic.config.main(argv=['upgrade', 'head'])


@_in_database_dir
def make_migrations():
    message = 'auto_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    alembic.config.main(argv=['revision', '--autogenerate', '-m', message])
