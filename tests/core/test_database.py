from tests.base import BaseTest

from app.core import database


class TestDatabase(BaseTest):
    def test_migration_not_fails(self):
        router = database.BaseModel.create_router()
        router.run()
