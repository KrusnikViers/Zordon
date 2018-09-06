from sqlalchemy import Column, Integer, ForeignKey, Table

from app.database.model import Base


group_members = Table('group_members', Base.metadata,
                      Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE')),
                      Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE')))
