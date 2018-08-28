import peewee
import peewee_migrate

from app.core import config


class BaseModel(peewee.Model):
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    class Meta:
        database = None

    @classmethod
    def connect_and_migrate(cls, credentials: dict):
        BaseModel.__dict__['_meta'].database = peewee.PostgresqlDatabase(**credentials)
        router = cls.create_router()
        router.run()

    @classmethod
    def create_router(cls) -> peewee_migrate.Router:
        migrations_dir = config.APP_DIRECTORY.joinpath('models', 'migrations')
        return peewee_migrate.Router(BaseModel.__dict__['_meta'].database,
                                     migrate_table='migrations',
                                     migrate_dir=str(migrations_dir))
