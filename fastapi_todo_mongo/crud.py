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
        logger.warning(f"Username {user.username} already exists")
        return None

    try:
        user_dict = {
            "username": user.username, 
            "password": hash_password(user.password)
        }
        result = await users_collection.insert_one(user_dict)
        
        # Return the user in the format expected by UserOut model
        new_user = {
            "id": str(result.inserted_id),
            "username": user.username
        }
        logger.info(f"Created new user: {user.username} with ID: {new_user['id']}")
        return new_user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return None
async def authenticate_user(username: str, password: str):
    users_collection = get_users_collection()
    if users_collection is None:
        logger.error("Cannot authenticate user - MongoDB not connected")
        return None

    user = await users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return None

    # Return in UserOut format
    return {
        "id": str(user["_id"]),
        "username": user["username"]
    }

# -------------------
# Todo CRUD
# -------------------
# In create_todo function:
async def create_todo(todo: TodoCreate, owner_id: str):
    todos_collection = get_todos_collection()
    if todos_collection is None:
        return None

    todo_dict = todo.model_dump()
    todo_dict["owner_id"] = owner_id
    result = await todos_collection.insert_one(todo_dict)
    
    # Return with id field instead of _id
    created_todo = await todos_collection.find_one({"_id": result.inserted_id})
    return {
        "id": str(created_todo["_id"]),
        "title": created_todo["title"],
        "description": created_todo.get("description"),
        "completed": created_todo.get("completed", False),
        "owner_id": created_todo["owner_id"]
    }

async def get_todo(todo_id: str, owner_id: str):
    todos_collection = get_todos_collection()
    if todos_collection is None:
        return None

    try:
        todo = await todos_collection.find_one({
            "_id": ObjectId(todo_id), 
            "owner_id": owner_id
        })
        if todo:
            return {
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo.get("description"),
                "completed": todo.get("completed", False),
                "owner_id": todo["owner_id"]
            }
        return None
    except:
        return None

async def get_todos(owner_id: str):
    todos_collection = get_todos_collection()
    if todos_collection is None:
        return []

    todos = []
    async for t in todos_collection.find({"owner_id": owner_id}):
        # Convert _id to id for the response model
        todo_data = {
            "id": str(t["_id"]),
            "title": t["title"],
            "description": t.get("description"),
            "completed": t.get("completed", False),
            "owner_id": t["owner_id"]
        }
        todos.append(todo_data)
    return todos


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
