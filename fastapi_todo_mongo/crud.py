from database import users_collection, todos_collection
from models import UserCreate, TodoCreate
from bson import ObjectId
from auth import hash_password
import asyncio

# User CRUD
async def create_user(user: UserCreate):
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        return None
    user_dict = {"username": user.username, "password": hash_password(user.password)}
    result = await users_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict

async def authenticate_user(username: str, password: str):
    user = await users_collection.find_one({"username": username})
    if not user:
        return None
    from auth import verify_password
    if not verify_password(password, user["password"]):
        return None
    user["id"] = str(user["_id"])
    return user

# Todo CRUD
async def create_todo(todo: TodoCreate, owner_id: str):
    todo_dict = todo.dict()
    todo_dict["owner_id"] = owner_id
    result = await todos_collection.insert_one(todo_dict)
    todo_dict["id"] = str(result.inserted_id)
    return todo_dict

async def get_todos(owner_id: str):
    todos = []
    async for t in todos_collection.find({"owner_id": owner_id}):
        t["id"] = str(t["_id"])
        todos.append(t)
    return todos

async def get_todo(todo_id: str, owner_id: str):
    todo = await todos_collection.find_one({"_id": ObjectId(todo_id), "owner_id": owner_id})
    if todo:
        todo["id"] = str(todo["_id"])
    return todo

async def update_todo(todo_id: str, data: dict, owner_id: str):
    await todos_collection.update_one({"_id": ObjectId(todo_id), "owner_id": owner_id}, {"$set": data})
    return await get_todo(todo_id, owner_id)

async def delete_todo(todo_id: str, owner_id: str):
    await todos_collection.delete_one({"_id": ObjectId(todo_id), "owner_id": owner_id})
    return {"message": "Todo deleted"}
