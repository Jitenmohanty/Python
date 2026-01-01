from bson import ObjectId
from config.database import todo_collection
from schemas.todo_schema import todo_serializer, todos_serializer

# Convert MongoDB document to JSON-serializable dict


# CRUD Operations
def create_todo(data):
    result = todo_collection.insert_one(data.dict())
    new_todo = todo_collection.find_one({"_id": result.inserted_id})
    return todo_serializer(new_todo)

def get_all_todos():
    todos = todo_collection.find()
    return todos_serializer(todos)

def get_todo_by_id(todo_id: str):
    todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
    return todo_serializer(todo) if todo else None

def update_todo(todo_id: str, data):
    todo_collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": data.dict(exclude_none=True)}
    )
    updated = todo_collection.find_one({"_id": ObjectId(todo_id)})
    return todo_serializer(updated) if updated else None

def delete_todo(todo_id: str):
    result = todo_collection.delete_one({"_id": ObjectId(todo_id)})
    return result.deleted_count > 0
