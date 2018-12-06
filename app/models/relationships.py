from sqlalchemy import BigInteger, Column, ForeignKey, Table

from app.database.base_model import Base

group_members = Table('group_members', Base.metadata,
                      Column('user_id', BigInteger, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE')),
                      Column('group_id', BigInteger, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE')))
