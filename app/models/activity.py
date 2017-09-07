import re

from peewee import ForeignKeyField, TextField

from app.models.base import BaseModel
from app.models.user import User


class Activity(BaseModel):
    """ Some activity, to which users can be invited """
    name = TextField(unique=True)
    owner = ForeignKeyField(User, on_delete='CASCADE')

    @classmethod
    def try_to_create(cls, new_activity_name: str, owner: User) -> (object, str):
        max_length = 25
        new_activity_name = new_activity_name.strip()
        if len(new_activity_name) > max_length:
            return None, 'name should be no longer than {0} characters.'.format(max_length)
        if len(new_activity_name) == 0:
            return None, 'name is empty.'
        if not re.match("^[\w\ \_\.\-]*$", new_activity_name):
            return None, 'allowed only alphanumeric characters, spaces and `_.-`'
        if cls.select().where(cls.name == new_activity_name).exists():
            return None, 'activity with name {0} already exists.'.format(new_activity_name)
        return cls.create(name=new_activity_name, owner=owner), ''

    @classmethod
    def try_to_get(cls, activity_name: str) -> (object, str):
        try:
            activity = Activity.get(Activity.name == activity_name)
        except Activity.DoesNotExist:
            return None, 'Activity {0} not found.'.format(activity_name)
        return activity, None

    def has_right_to_remove(self, user: User):
        if user.has_right_to('a_delete'):
            return self.owner == user or user.is_superuser()
        return False
