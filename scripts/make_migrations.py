from app.settings import about, database


database.router.create(name='auto_' + str(about.version_major), auto='app.models.all')
database.router.run()
