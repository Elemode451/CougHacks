# main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
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

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Socket.IO ASGI app
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# CORS (if you're using frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def join_room(sid, data):

    print("join_room received:", data)


    room = data["room"]
    db: Session = SessionLocal()

    # validate room exists
    chatroom = db.query(Chatroom).filter_by(slug=room).first()
    if not chatroom:
        await sio.emit("error", {"message": f"Chatroom '{room}' does not exist"}, to=sid)
        return

    # add user to room
    await sio.enter_room(sid, room)

    # fetch last 30 messages from this room
    messages = (
        db.query(Message)
        .filter_by(room_slug=room)
        .order_by(Message.timestamp.desc())
        .limit(30)
        .all()
    )

    # reverse to show oldest → newest
    messages.reverse()

    # send message history to just the joining client
    await sio.emit("chat_history", [
        {
            "uid": msg.user_uid,
            "sender": msg.user.nickname,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ], to=sid)

    await sio.emit("user_joined", {"sid": sid}, room=room, skip_sid=sid)


@sio.event
async def send_message(sid, data):

    print("send_message received:", data)

    room_slug = data["room"]
    user_uid = data["uid"]
    content = data["content"]

    db: Session = SessionLocal()

    chatroom = db.query(Chatroom).filter_by(slug=room_slug).first()
    if not chatroom:
        await sio.emit("error", {"message": f"Chatroom '{room_slug}' does not exist"}, to=sid)
        return

    user = db.query(User).filter_by(uid=user_uid).first()
    if not user:
        await sio.emit("error", {"message": f"User '{user_uid}' does not exist"}, to=sid)
        return

    timestamp = datetime.utcnow()
    message = Message(
        room_slug=room_slug,
        user_uid=user_uid,
        content=content,
        timestamp=timestamp
    )
    db.add(message)
    db.commit()

    await sio.emit("chat_message", {
        "uid": user_uid,
        "sender": user.nickname,
        "content": content,
        "timestamp": timestamp.isoformat()
    }, room=room_slug, skip_sid=sid)



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
    file_path = os.path.join(os.path.dirname(__file__), "temp.html")
    print(file_path)
    return FileResponse(path=file_path, media_type='text/html')

@app.get("/chatrooms")
async def get_chatrooms():
    db = SessionLocal()
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
    uvicorn.run("main:socket_app", host="0.0.0.0", port=8000, reload=True)

