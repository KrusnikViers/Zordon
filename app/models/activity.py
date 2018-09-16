from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.model import Base
from app.models.relationships import activity_participants


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    locale = Column(String, nullable=True)

    users = relationship("User", secondary=activity_participants, back_populates='activities')
