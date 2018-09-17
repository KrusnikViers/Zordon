from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_model import Base
from app.models.relationships import group_members


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    locale = Column(String, nullable=True)

    users = relationship("User", secondary=group_members, back_populates='groups')
