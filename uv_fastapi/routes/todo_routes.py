from fastapi import APIRouter, HTTPException, Header
from models.todo_model import TodoModel
from controller.todo_controller import (
    create_todo, get_all_todos, get_todo_by_id, update_todo, delete_todo
)
from utils.jwt_handler import verify_token

router = APIRouter(prefix="/todos", tags=["Todo CRUD"])

@router.post("/")
def add_todo(item: TodoModel, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1] if Authorization else None
    if not token:
        raise HTTPException(401, "Authorization token required")
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(401, "Invalid or expired token")
    return create_todo(item)

@router.get("/")
def list_todos():
    return get_all_todos()

@router.get("/{todo_id}")
def get_single(todo_id: str):
    todo = get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(404, "Todo Not Found")
    return todo

@router.put("/{todo_id}")
def edit(todo_id: str, item: TodoModel, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1] if Authorization else None
    if not token:
        raise HTTPException(401, "Authorization token required")
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(401, "Invalid or expired token")
    todo = update_todo(todo_id, item)
    if not todo:
        raise HTTPException(404, "Todo Not Found")
    return todo

@router.delete("/{todo_id}")
def remove(todo_id: str, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1] if Authorization else None
    if not token:
        raise HTTPException(401, "Authorization token required")
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(401, "Invalid or expired token")
    deleted = delete_todo(todo_id)
    if not deleted:
        raise HTTPException(404, "Todo Not Found")
    return {"message": "Todo Deleted Successfully"}
