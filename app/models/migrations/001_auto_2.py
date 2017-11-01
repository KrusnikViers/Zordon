"""Peewee migrations -- 001_auto_2.py.

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


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class User(pw.Model):
        telegram_id = pw.IntegerField(unique=True)
        login = pw.TextField(default='')
        rights = pw.IntegerField(default=0)
        status = pw.IntegerField(default=1)
        pending_action = pw.IntegerField(default=0)

        class Meta:
            db_table = "user"

    @migrator.create_model
    class Activity(pw.Model):
        name = pw.TextField(unique=True)
        owner = pw.ForeignKeyField(db_column='owner_id', on_delete='CASCADE', rel_model=migrator.orm['user'], to_field='id')
        is_public = pw.BooleanField(default=True)
        last_call = pw.TimestampField(default=dt.datetime.now, null=True)

        class Meta:
            db_table = "activity"

    @migrator.create_model
    class ActivityAccess(pw.Model):
        user = pw.ForeignKeyField(db_column='user_id', on_delete='CASCADE', rel_model=migrator.orm['user'], to_field='id')
        activity = pw.ForeignKeyField(db_column='activity_id', on_delete='CASCADE', rel_model=migrator.orm['activity'], to_field='id')

        class Meta:
            db_table = "activityaccess"

    @migrator.create_model
    class Subscription(pw.Model):
        user = pw.ForeignKeyField(db_column='user_id', on_delete='CASCADE', rel_model=migrator.orm['user'], to_field='id')
        activity = pw.ForeignKeyField(db_column='activity_id', on_delete='CASCADE', rel_model=migrator.orm['activity'], to_field='id')
        reply_state = pw.IntegerField(default=0)
        reply_time = pw.TimestampField(default=dt.datetime.now)
        reply_message = pw.TextField(null=True)

        class Meta:
            db_table = "subscription"



def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('subscription')

    migrator.remove_model('activityaccess')

    migrator.remove_model('activity')

    migrator.remove_model('user')
