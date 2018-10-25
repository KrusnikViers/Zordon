from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.base_model import Base


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    title = Column(String, nullable=False)

    author = relationship("User", back_populates="requests")
    responses = relationship("Response")
