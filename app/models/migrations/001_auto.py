"""Peewee migrations -- 001_auto.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class Activity(pw.Model):
        id = pw.IntegerField(primary_key=True)
        name = pw.TextField()

        class Meta:
            table_name = "activities"

    @migrator.create_model
    class BaseModel(pw.Model):
        id = pw.AutoField()

        class Meta:
            table_name = "basemodel"

    @migrator.create_model
    class Group(pw.Model):
        tg_chat_id = pw.IntegerField(primary_key=True)
        name = pw.TextField()
        locale = pw.TextField()

        class Meta:
            table_name = "groups"

    @migrator.create_model
    class User(pw.Model):
        tg_user_id = pw.IntegerField(primary_key=True)
        tg_login = pw.TextField(unique=True)
        visible_name = pw.TextField()
        locale = pw.TextField()
        is_mute_enabled = pw.BooleanField()

        class Meta:
            table_name = "users"

    @migrator.create_model
    class GroupMember(pw.Model):
        user = pw.ForeignKeyField(backref='groupmember_set', column_name='user_id', field='tg_user_id', model=migrator.orm['users'])
        group = pw.ForeignKeyField(backref='groupmember_set', column_name='group_id', field='tg_chat_id', model=migrator.orm['groups'])

        class Meta:
            table_name = "group_members"

            primary_key = pw.CompositeKey('user', 'group')

    @migrator.create_model
    class Participant(pw.Model):
        activity = pw.ForeignKeyField(backref='participant_set', column_name='activity_id', field='id', model=migrator.orm['activities'])
        user = pw.ForeignKeyField(backref='participant_set', column_name='user_id', field='tg_user_id', model=migrator.orm['users'])

        class Meta:
            table_name = "participants"

            primary_key = pw.CompositeKey('activity', 'user')



def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('users')

    migrator.remove_model('participants')

    migrator.remove_model('group_members')

    migrator.remove_model('groups')

    migrator.remove_model('basemodel')

    migrator.remove_model('activities')
