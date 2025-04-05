# models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    uid = Column(String, primary_key=True)
    nickname = Column(String, nullable=False)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

    messages = relationship('Message', back_populates='user')

class Chatroom(Base):
    __tablename__ = 'chatrooms'

    slug = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    mode = Column(String, nullable=False)

    messages = relationship('Message', back_populates='chatroom')

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_slug = Column(String, ForeignKey('chatrooms.slug'), nullable=False)
    user_uid = Column(String, ForeignKey('users.uid'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    chatroom = relationship('Chatroom', back_populates='messages')
    user = relationship('User', back_populates='messages')
