from database import get_users_collection, get_todos_collection
from models import UserCreate, TodoCreate
from bson import ObjectId
from auth import hash_password, verify_password
import logging

logger = logging.getLogger(__name__)

# -------------------
# User CRUD
# -------------------
async def create_user(user: UserCreate):
    users_collection = get_users_collection()
    if users_collection is None:
        logger.error("Cannot create user - MongoDB not connected")
        return None

    existing = await users_collection.find_one({"username": user.username})
    if existing:
        return None

    user_dict = {"username": user.username, "password": hash_password(user.password)}
    result = await users_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    logger.info(f"Created new user: {user.username}")
    return user_dict


async def authenticate_user(username: str, password: str):
    users_collection = get_users_collection()
    if users_collection is None:
        logger.error("Cannot authenticate user - MongoDB not connected")
        return None

    user = await users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return None

    user["id"] = str(user["_id"])
    return user

# -------------------
# Todo CRUD
# -------------------
async def create_todo(todo: TodoCreate, owner_id: str):
    todos_collection = get_todos_collection()
    if todos_collection is None:
        logger.error("Cannot create todo - MongoDB not connected")
        return None

    todo_dict = todo.dict()
    todo_dict["owner_id"] = owner_id
    result = await todos_collection.insert_one(todo_dict)
    todo_dict["id"] = str(result.inserted_id)
    logger.info(f"Created new todo for user: {owner_id}")
    return todo_dict


async def get_todos(owner_id: str):
    todos_collection = get_todos_collection()
    if todos_collection is None:
        logger.error("Cannot get todos - MongoDB not connected")
        return []

    todos = []
    async for t in todos_collection.find({"owner_id": owner_id}):
        t["id"] = str(t["_id"])
        todos.append(t)
    return todos


async def get_todo(todo_id: str, owner_id: str):
    todos_collection = get_todos_collection()
    if todos_collection is None:
        return None

    todo = await todos_collection.find_one({"_id": ObjectId(todo_id), "owner_id": owner_id})
    if todo:
        todo["id"] = str(todo["_id"])
    return todo


async def update_todo(todo_id: str, data: dict, owner_id: str):
    todos_collection = get_todos_collection()
    if todos_collection is None:
        return None

    await todos_collection.update_one(
        {"_id": ObjectId(todo_id), "owner_id": owner_id},
        {"$set": data}
    )
    return await get_todo(todo_id, owner_id)


async def delete_todo(todo_id: str, owner_id: str):
    todos_collection = get_todos_collection()
    if todos_collection is None:
        return {"message": "Database not available"}

    await todos_collection.delete_one({"_id": ObjectId(todo_id), "owner_id": owner_id})
    return {"message": "Todo deleted"}
