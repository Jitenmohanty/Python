from bson import ObjectId
from config.database import db
from utils.hash import hash_password, verify_password
from utils.jwt_handler import create_token
from schemas.user_schema import user_serializer

user_collection = db.users

def register_user(data):
    if user_collection.find_one({"email": data.email}):
        return {"error": "Email already registered"}

    data.password = hash_password(data.password)
    user_collection.insert_one(data.dict())
    return {"message": "User registered successfully"}

def login_user(email: str, password: str):
    user = user_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return {"error": "Invalid email or password"}

    token = create_token(str(user["_id"]))
    return {"token": token, "user": user_serializer(user)}

def get_profile(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    return user_serializer(user) if user else None

def update_profile(user_id: str, data):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    updated = user_collection.find_one({"_id": ObjectId(user_id)})
    return user_serializer(updated)
