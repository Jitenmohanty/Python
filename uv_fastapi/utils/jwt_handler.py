import time
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret123")
ALGORITHM = "HS256"

def create_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": time.time() + 3600  # valid 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded["user_id"]
    except:
        return None
