from os.path import dirname, realpath, sep
import peewee
import peewee_migrate

from app.base import settings


def _get_database():
    database = peewee.PostgresqlDatabase(settings.database['NAME'],
                                         user=settings.database['USER'],
                                         password=settings.database['PASSWORD'],
                                         host=settings.database['HOST'],
                                         port=settings.database['PORT'])
    # Run migrations after connection established
    router = peewee_migrate.Router(database, migrate_dir=dirname(realpath(__file__)) + sep + "migrations")
    router.run()
    return database


class BaseModel(peewee.Model):
    """ Base model, that uses PostgreSQL database """
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    class Meta:
        database = _get_database()
