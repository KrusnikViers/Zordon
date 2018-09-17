from sqlalchemy import Column, Integer, ForeignKey, Table

from app.database.base_model import Base


group_members = Table('group_members', Base.metadata,
                      Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE')),
                      Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE')))

activity_participants = Table('activity_participants', Base.metadata,
                              Column('user_id', Integer,
                                     ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE')),
                              Column('activity_id', Integer,
                                     ForeignKey('activities.id', ondelete='CASCADE', onupdate='CASCADE')))
