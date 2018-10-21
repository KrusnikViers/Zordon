from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.base_model import Base


REQUEST_TYPES = ['call']


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    answer = Column(Integer, nullable=False)
    type = Column(String, nullable=False)

    user = relationship("User", back_populates="responses")
