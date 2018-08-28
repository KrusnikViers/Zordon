from app.core import config, database


config.load_user_configuration()
database.initialise()

router = database.create_router()
router.create(name='auto', auto='app.models')
router.run()
