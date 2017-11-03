from app.common import project_info, database


database.router.create(name='auto_' + str(project_info.version_major), auto='app.models.all')
database.router.run()
