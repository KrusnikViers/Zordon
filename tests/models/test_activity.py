from app.definitions import superuser_login
from app.models.activity import Activity
from app.models.user import User
from tests.base_test import BaseTestCase


class TestActivityModel(BaseTestCase):
    def test_try_to_create_basic(self):
        user = User.create(telegram_user_id=0)
        result = Activity.try_to_create('Correct name', user)[0]
        self.assertNotEqual(None, result)
        self.assertEqual('Correct name', result.name)
        self.assertEqual(user, result.owner)

    def test_try_to_create_wrong_length(self):
        user = User.create(telegram_user_id=0)
        result = Activity.try_to_create('Too many letters obviously', user)[0]
        self.assertEqual(None, result)

    def test_try_to_create_empty(self):
        user = User.create(telegram_user_id=0)
        result = Activity.try_to_create('    ', user)[0]
        self.assertEqual(None, result)

    def test_try_to_create_bad_characters(self):
        user = User.create(telegram_user_id=0)
        result = Activity.try_to_create('Why, mr Andersen?', user)[0]
        self.assertEqual(None, result)

    def test_try_to_create_already_exists(self):
        user = User.create(telegram_user_id=0)
        activity = Activity.try_to_create('Im fine', user)[0]
        self.assertNotEqual(None, activity)
        result = Activity.try_to_create('Im fine', user)[0]
        self.assertEqual(None, result)

    def test_has_right_to_remove_owner(self):
        user = User.create(telegram_user_id=0)
        superuser = User.create(telegram_user_id=1, telegram_login=superuser_login)
        another_user = User.create(telegram_user_id=2)
        activity = Activity.try_to_create('Correct name', user)[0]
        self.assertFalse(activity.has_right_to_remove(user))
        self.assertTrue(activity.has_right_to_remove(superuser))
        self.assertFalse(activity.has_right_to_remove(another_user))

    def test_try_to_get_basic(self):
        user = User.create(telegram_user_id=0)
        activity = Activity.create(name='TestActivity', owner=user)

        result, error = Activity.try_to_get('TestActivity')
        self.assertEqual(activity, result)
        self.assertFalse(error)

    def test_try_to_get_not_existing(self):
        result, error = Activity.try_to_get('NonExistingActivity')
        self.assertEqual(None, result)
        self.assertTrue(error)
