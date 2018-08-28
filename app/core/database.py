import dj_database_url
import peewee
import peewee_migrate

from app.core import config


_database = None


class BaseModel(peewee.Model):
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    class Meta:
        database = None


def initialise():
    global _database
    credentials = dj_database_url.parse(config.DATABASE_URL)
    _database = peewee.PostgresqlDatabase(credentials['NAME'],
                                          user=credentials['USER'], password=credentials['PASSWORD'],
                                          host=credentials['HOST'], port=credentials['PORT'])
    BaseModel.__dict__['_meta'].database = _database
    create_router().run()


def create_router() -> peewee_migrate.Router:
    migrations_dir = config.APP_DIRECTORY.joinpath('models', 'migrations')
    return peewee_migrate.Router(_database, migrate_table='migrations', migrate_dir=str(migrations_dir))
