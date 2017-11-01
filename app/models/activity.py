from enum import Enum
from peewee import BooleanField, ForeignKeyField, TextField, TimestampField
import re

from app.settings import database
from app.models.user import User


class Activity(database.BaseModel):
    # Fields.
    name = TextField(unique=True)
    owner = ForeignKeyField(User, on_delete='CASCADE')
    is_public = BooleanField(default=True)
    last_call = TimestampField(null=True)

    # Name validation for activities to be created.
    class NameValidationResult(Enum):
        ok = 0
        too_long = 1
        name_empty = 2
        invalid_characters = 3
        already_exists = 4

    @classmethod
    def validate_name(cls, new_activity_name) -> NameValidationResult:
        new_activity_name = new_activity_name.strip()
        max_length = 25
        if len(new_activity_name) > max_length:
            return cls.NameValidationResult.too_long
        if len(new_activity_name):
            return cls.NameValidationResult.name_empty
        if not re.match("^[\w\ \_\.\-]*$", new_activity_name):
            return cls.NameValidationResult.invalid_characters
        if cls.select().where(cls.name == new_activity_name).exists():
            return cls.NameValidationResult.already_exists
        return cls.NameValidationResult.ok
