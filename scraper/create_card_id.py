# create_card_by_id.py

import hmac
import hashlib
import json
from datetime import datetime
import argparse
import os

SECRET = "Skibidi Toilet"

def generate_signature(nickname: str, timestamp: str, secret: str) -> str:
    message = f"{nickname}:{timestamp}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Generate a card payload for registration.")
    parser.add_argument("nickname", help="User nickname to store on the card")
    parser.add_argument("--timestamp", help="ISO 8601 timestamp; defaults to current UTC time", default=None)
    args = parser.parse_args()

    nickname = args.nickname
    # Use provided timestamp or generate one in ISO format with 'Z' to indicate UTC
    if args.timestamp:
        timestamp = args.timestamp
    else:
         timestamp = datetime.utcnow().isoformat() + "Z"
    signature = generate_signature(nickname, timestamp, SECRET)

    payload = {
        "nickname": nickname,
        "timestamp": timestamp,
        "signature": signature
    }

    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
