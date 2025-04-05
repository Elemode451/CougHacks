from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    uid = Column(String, primary_key=True)  # TEXT -> String
    nickname = Column(String, nullable=False)  # TEXT NOT NULL -> String NOT NULL

    # Optional relationship to messages
    messages = relationship('Message', back_populates='user')

class Chatroom(Base):
    __tablename__ = 'chatrooms'

    slug = Column(String, primary_key=True)  # TEXT -> String
    name = Column(String, nullable=False)  # TEXT NOT NULL -> String NOT NULL
    mode = Column(String, nullable=False)  # TEXT NOT NULL -> String NOT NULL

    # Optional relationship to messages
    messages = relationship('Message', back_populates='chatroom')

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)  # INTEGER PRIMARY KEY AUTOINCREMENT -> Integer
    room_slug = Column(String, ForeignKey('chatrooms.slug'), nullable=False)  # room_slug (FK to chatrooms)
    user_uid = Column(String, ForeignKey('users.uid'), nullable=False)  # user_uid (FK to users)
    content = Column(Text, nullable=False)  # TEXT NOT NULL -> Text NOT NULL
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  # DATETIME DEFAULT CURRENT_TIMESTAMP

    # Relationships
    chatroom = relationship('Chatroom', back_populates='messages')
    user = relationship('User', back_populates='messages')

# Database connection URL (adjust based on your setup)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Now you can interact with your database using SQLAlchemy ORM