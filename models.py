from sqlalchemy import Column, String, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True)
    nickname = Column(String, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)