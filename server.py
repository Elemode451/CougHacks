# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Any
import json
import asyncio
import uuid
from datetime import datetime
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory data store (in a real app, you'd use a database)
connected_users: Dict[str, Dict[str, Any]] = {}
active_connections: Dict[str, WebSocket] = {}
channels = [
    {"id": 1, "name": "general", "messages": []},
    {"id": 2, "name": "random", "messages": []},
    {"id": 3, "name": "introductions", "messages": []},
]

# Channel subscriptions
channel_subscriptions: Dict[int, List[str]] = {1: [], 2: [], 3: []}


class ConnectionManager:
    """
    Manages WebSocket connections and broadcasts messages
    """

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        active_connections[client_id] = websocket

    async def disconnect(self, client_id: str):
        if client_id in active_connections:
            del active_connections[client_id]

        # Remove user from channel subscriptions
        for channel_id in channel_subscriptions:
            if client_id in channel_subscriptions[channel_id]:
                channel_subscriptions[channel_id].remove(client_id)

        # Notify others that user has left
        if client_id in connected_users:
            await self.broadcast_user_left(connected_users[client_id])
            del connected_users[client_id]

    async def send_personal_message(self, message: dict, client_id: str):
        if client_id in active_connections:
            await active_connections[client_id].send_json(message)

    async def broadcast(self, message: dict, exclude: Optional[str] = None):
        for client_id, connection in active_connections.items():
            if exclude is None or client_id != exclude:
                await connection.send_json(message)

    async def broadcast_to_channel(self, channel_id: int, message: dict, exclude: Optional[str] = None):
        if channel_id in channel_subscriptions:
            for client_id in channel_subscriptions[channel_id]:
                if exclude is None or client_id != exclude:
                    if client_id in active_connections:
                        await active_connections[client_id].send_json(message)

    async def broadcast_user_joined(self, user: dict):
        await self.broadcast({
            "type": "user_joined",
            "data": user
        })

    async def broadcast_user_left(self, user: dict):
        await self.broadcast({
            "type": "user_left",
            "data": user
        })

    async def broadcast_new_channel(self, channel: dict):
        await self.broadcast({
            "type": "new_channel",
            "data": channel
        })


# Create connection manager instance
manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)

    try:
        while True:
            # Receive JSON data from the client
            data = await websocket.receive_text()
            message = json.loads(data)
            message_type = message.get("type") # Sends a JSON with type field, data field

            if message_type == "login":
                # Process login
                user_data = message.get("data", {})
                user = {
                    "id": user_data.get("id", client_id),
                    "username": user_data.get("username"),
                    "avatar": user_data.get("avatar")
                }

                # sqlalchemy.send("to the database ")

                # Save user
                connected_users[client_id] = user

                # Send login success with channels
                await manager.send_personal_message({
                    "type": "login_success",
                    "data": {
                        "user": user,
                        "channels": channels
                    }
                }, client_id)

                # Broadcast new user to all connected clients
                await manager.broadcast_user_joined(user)
                print(f"User logged in: {user['username']}")

            elif message_type == "send_message":
                # Process send message
                message_data = message.get("data", {})
                channel_id = message_data.get("channelId")
                message_text = message_data.get("message")

                user = connected_users.get(client_id)

                if user and channel_id is not None:
                    new_message = {
                        "id": str(uuid.uuid4()),
                        "text": message_text,
                        "timestamp": datetime.now().isoformat(),
                        "user": user
                    }

                    channel = next((c for c in channels if c["id"] == channel_id), None)
                    if channel:
                        channel["messages"].append(new_message)

                        # Broadcast message to all users in the channel
                        await manager.broadcast_to_channel(channel_id, {
                            "type": "new_message",
                            "data": {
                                "channelId": channel_id,
                                "message": new_message
                            }
                        })

                        print(f"New message in {channel['name']} from {user['username']}")

            elif message_type == "create_channel":
                channel_name = message.get("data")

                if channel_name:
                    # Create new channel
                    new_channel = {
                        "id": len(channels) + 1,
                        "name": channel_name.lower().replace(" ", "-"),
                        "messages": []
                    }

                    channels.append(new_channel)
                    channel_subscriptions[new_channel["id"]] = []

                    # Broadcast new channel to all connected clients
                    await manager.broadcast_new_channel(new_channel)
                    print(f"New channel created: {new_channel['name']}")

    except WebSocketDisconnect:
        await manager.disconnect(client_id)
    except Exception as e:
        print(f"Error: {e}")
        await manager.disconnect(client_id)


@app.get("/api/channels")
async def get_channels():
    return channels


@app.get("/api/channels/{channel_id}")
async def get_channel(channel_id: int):
    channel = next((c for c in channels if c["id"] == channel_id), None)

    if not channel:
        return {"error": "Channel not found"}, 404

    return channel


# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)