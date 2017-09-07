from os.path import dirname, realpath, sep
import datetime
import peewee as pw
import peewee_migrate as pwm

from app.definitions import database_credentials


def _get_database():
    database = pw.PostgresqlDatabase(database_credentials['NAME'],
                                     user=database_credentials['USER'],
                                     password=database_credentials['PASSWORD'],
                                     host=database_credentials['HOST'],
                                     port=database_credentials['PORT'])
    # Run migrations after connection established
    router = pwm.Router(database, migrate_dir=dirname(realpath(__file__)) + sep + "migrations")
    router.run()
    return database


class BaseModel(pw.Model):
    """ Base model, that uses PostgreSQL database """
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    class Meta:
        database = _get_database()
