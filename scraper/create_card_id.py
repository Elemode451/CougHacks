# create_card_by_id.py

import hmac
import hashlib
import json
from datetime import datetime
import argparse
import os

SECRET = "5c2e0e5f5b31f523db2670462038c87930bd5397af439bbc4ecae2b8e95fddf5"

def generate_signature(nickname: str, timestamp: str, secret: str) -> str:
    message = f"{nickname}:{timestamp}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()

def generate():
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

    return payload

if __name__ == "__main__":
    generate()
