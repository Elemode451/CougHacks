# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
from database import Base, engine, SessionLocal
from models import User
from datetime import datetime
import hmac, hashlib, os

SECRET = "Skibidi Toilet"
app = FastAPI()

Base.metadata.create_all(bind=engine)

#pydantic
class CardPayload(BaseModel):
    nickname: str
    timestamp: str
    signature: str

# Function to generate a signature using HMAC-SHA256
def generate_signature(nickname: str, timestamp: str, secret: str) -> str:
    message = f"{nickname}:{timestamp}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()

@app.get("/")
async def root():
    return {"message": "pranav"}

@app.get("/dev/users")
async def get_users(): 
    db: Session = SessionLocal()
    users = db.query(User).all()
    # Convert SQLAlchemy User objects to dictionaries
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

