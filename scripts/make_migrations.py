from app.core import config, database


config.load_user_configuration()
database.BaseModel.connect_and_migrate(config.DATABASE_CREDENTIALS)

router = database.BaseModel.create_router()
router.create(name='auto', auto='app.models')
router.run()
