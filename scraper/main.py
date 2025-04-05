# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import hmac, hashlib, os

# config

SECRET = os.getenv("DARKLINE_SECRET", "dev-fallback-secret")
DB = "sqlite:///./offline.db"


Base = declarative_base()
engine = create_engine(DB, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True)
    nickname = Column(String, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)


app = FastAPI()
Base.metadata.create_all(bind=engine)


class CardPayload(BaseModel):
    nickname: str
    timestamp: str
    signature: str


def generate_signature(nickname: str, timestamp: str, secret: str) -> str:
    message = f"{nickname}:{timestamp}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


@app.post("/register")
async def register_user(payload: CardPayload):
    expected = generate_signature(payload.nickname, payload.timestamp, SECRET)

    if not hmac.compare_digest(expected, payload.signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    uid = payload.signature[:12]

    db: Session = SessionLocal()
    user = db.query(User).filter_by(uid=uid).first()

    if user:
        return {
            "uid": user.uid,
            "nickname": user.nickname,
            "message": "Already registered"
        }

    new_user = User(
        uid=uid,
        nickname=payload.nickname,
        registered_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()

    return {
        "uid": uid,
        "nickname": payload.nickname,
        "message": "Registered successfully"
    }
