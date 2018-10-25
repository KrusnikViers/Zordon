from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.base_model import Base


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    request_id = Column(Integer, ForeignKey('requests.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    answer = Column(Integer, nullable=False)

    user = relationship("User", back_populates="responses")
    request = relationship("Request", back_populates="responses")
