from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.model import Base
from app.models.relationships import activity_participants, group_members


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    name = Column(String, nullable=False)

    is_mute_enabled = Column(Boolean, nullable=False, default=False)
    locale = Column(String, nullable=True)

    groups = relationship("Groups", secondary=group_members, back_populates='users')
    activities = relationship("Activities", secondary=activity_participants, back_populates='users')
