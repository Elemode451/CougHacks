from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User
from datetime import datetime
import hmac, hashlib, os

SECRET = "Skibidi Toilet"
app = FastAPI()
Base.metadata.create_all(bind=engine)

class CardPayload(BaseModel):
    nickname: str
    timestamp: str
    signature: str

def generate_signature(nickname: str, timestamp: str, secret: str) -> str:
    msg = f"{nickname}:{timestamp}".encode()
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()


@app.get("/") 
async def root():
    return {"message" : "i love Pranav"}



@app.post("/register")
async def register_user(payload: CardPayload):
    expected = generate_signature(payload.nickname, payload.timestamp, SECRET)

    if not hmac.compare_digest(expected, payload.signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    uid = payload.signature[:12]
    db: Session = SessionLocal()

    user = db.query(User).filter_by(uid=uid).first()
    if user:
        return {"uid": user.uid, "nickname": user.nickname, "message": "Already registered"}

    new_user = User(uid=uid, nickname=payload.nickname, registered_at=datetime.utcnow())
    db.add(new_user)
    db.commit()

    return {"uid": uid, "nickname": payload.nickname, "message": "Registered successfully"}
