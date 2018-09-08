import os
import sys

from app.core.info import APP_DIR
from app.database.migrations import router
from tests.base import DatabaseTestCase


class PrintSuppressor:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class TestDatabase(DatabaseTestCase):
    def test_connection(self):
        self.assertIsNotNone(self.connection.engine)
        with self.connection.engine.connect():
            pass

    def test_nothing_to_autodetect(self):
        migrations_dir = APP_DIR.joinpath('database', 'migrations', 'versions')

        # Generate new migration and make sure it was generated.test
        old_migrations_list = sorted(os.listdir(migrations_dir))
        with PrintSuppressor():
            router.make_migrations(self.connection.engine)
        new_migrations = [file for file in os.listdir(migrations_dir) if file not in old_migrations_list]
        self.assertEqual(1, len(new_migrations))

        # Get migration file contents, removing migration file itself.
        migration_file_path = str(migrations_dir.joinpath(new_migrations[0]))
        with open(migration_file_path, 'r') as migration_file:
            migration_contents = migration_file.read().replace('\n', ' ').split()
        os.remove(migration_file_path)

        # Check that migration body contains |pass| for both upgrade and downgrade methods.
        commands_sequence = ['upgrade():', 'pass', 'downgrade():', 'pass']
        self.assertEqual(commands_sequence,
                         [command for command in migration_contents if command in commands_sequence])
