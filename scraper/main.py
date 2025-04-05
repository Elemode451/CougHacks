# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
from database import Base, engine, SessionLocal
from models import User, Chatroom, Message
from datetime import datetime
import hmac, hashlib, os

SECRET = "Skibidi Toilet"
app = FastAPI()

Base.metadata.create_all(bind=engine)

class CardPayload(BaseModel):
    nickname: str
    timestamp: str
    signature: str

class CreateChatroomPayload(BaseModel):
    slug: str
    name: str
    mode: str 

def generate_signature(nickname: str, timestamp: str, secret: str) -> str:
    message = f"{nickname}:{timestamp}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()

@app.get("/")
async def root():
    return {"message": "pranav"}


@app.get("/chatrooms")
async def get_chatrooms():
    db: Session = SessionLocal()
    chatrooms = db.query(Chatroom).all()
    return [
        {"slug": room.slug, "name": room.name, "mode": room.mode}
        for room in chatrooms
    ]


@app.post("/chatrooms")
async def create_chatroom(payload: CreateChatroomPayload):
    db: Session = SessionLocal()
    existing = db.query(Chatroom).filter_by(slug=payload.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Chatroom already exists")

    new_room = Chatroom(slug=payload.slug, name=payload.name, mode=payload.mode)
    db.add(new_room)
    db.commit()
    return {"message": "Chatroom created", "slug": new_room.slug}




@app.get("/dev/users")
async def get_users(): 
    db: Session = SessionLocal()
    users = db.query(User).all()

    return [
        {
            "uid": user.uid,
            "nickname": user.nickname,
            "registered_at": user.registered_at.isoformat() if user.registered_at else None
        }
        for user in users
    ]

@app.post("/register")
async def register_user(payload: CardPayload):
    expected_signature = generate_signature(payload.nickname, payload.timestamp, SECRET)
    print(expected_signature)
    print(payload.signature)
    if not hmac.compare_digest(expected_signature, payload.signature):
        raise HTTPException(
            status_code=403, 
            detail=f"Invalid signature. Expected: {expected_signature}, received: {payload.signature}"
        )
    
    uid = payload.signature[:12]
    
    # Create a new database session and try to fetch the user
    db: Session = SessionLocal()
    user = db.query(User).filter_by(uid=uid).first()
    if user:
        return {"uid": user.uid, "nickname": user.nickname, "message": "Already registered"}
    
    # If the user doesn't exist, create a new one
    new_user = User(uid=uid, nickname=payload.nickname, registered_at=datetime.utcnow())
    db.add(new_user)
    db.commit()
    
    return {"uid": uid, "nickname": payload.nickname, "message": "Registered successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

