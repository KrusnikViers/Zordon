from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.base_model import Base


class Response(Base):
    __tablename__ = 'responses'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    request_id = Column(BigInteger, ForeignKey('requests.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    answer = Column(BigInteger, nullable=False)

    user = relationship("User", back_populates="responses")
    request = relationship("Request", back_populates="responses")
