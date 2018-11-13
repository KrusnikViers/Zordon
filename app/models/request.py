from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.base_model import Base


class Request(Base):
    __tablename__ = 'requests'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger, nullable=False)
    chat_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    author_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    title = Column(String, nullable=False)

    author = relationship("User", back_populates="requests")
    responses = relationship("Response")
