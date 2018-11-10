from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_model import Base
from app.models.relationships import group_members


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    name = Column(String, nullable=False)

    is_mute_enabled = Column(Boolean, nullable=False, default=False)
    is_known = Column(Boolean, nullable=False, default=False)
    locale = Column(String, nullable=True)

    groups = relationship("Group", secondary=group_members, back_populates='users')
    requests = relationship("Request")
    responses = relationship("Response")
