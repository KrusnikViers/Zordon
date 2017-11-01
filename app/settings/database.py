import dj_database_url
import pathlib
import peewee
import peewee_migrate
import os


# Establish connection with database and run pending migrations
_credentials = dj_database_url.parse(os.environ['ZORDON_DATABASE'])
database = peewee.PostgresqlDatabase(_credentials['NAME'],
                                     user=_credentials['USER'], password=_credentials['PASSWORD'],
                                     host=_credentials['HOST'], port=_credentials['PORT'])
_migrations_dir = str(pathlib.Path(os.path.realpath(__file__)).parent.parent.joinpath('models', 'migrations'))
router = peewee_migrate.Router(database, migrate_table='migrations', migrate_dir=_migrations_dir)
router.run()

# This variables will not be used any more.
del _migrations_dir
del _credentials


class BaseModel(peewee.Model):
    """ Base model, that uses PostgreSQL database """
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    class Meta:
        database = database

    @classmethod
    def maybe_get(cls, *args, **kwargs) -> object:
        try:
            result = cls.get(*args, **kwargs)
        except cls.DoesNotExist:
            return None
        return result
