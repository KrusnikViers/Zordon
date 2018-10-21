from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.base_model import Base


REQUEST_TYPES = ['call']


class Request(Base):
    __tablename__ = 'requests'

    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    type = Column(String, nullable=False)

    author = relationship("User", back_populates="requests")
