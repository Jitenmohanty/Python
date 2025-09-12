from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import UserCreate, UserOut, TodoCreate, TodoOut, Token
from crud import create_user, authenticate_user, create_todo, get_todos, get_todo, update_todo, delete_todo
from auth import create_access_token, decode_access_token
from typing import List

app = FastAPI(title="FastAPI Todo App with MongoDB")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT auth dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user_id

# Register
@app.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    new_user = await create_user(user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return new_user

# Login
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": str(user["id"])})
    return {"access_token": access_token, "token_type": "bearer"}

# Create Todo
@app.post("/todos", response_model=TodoOut)
async def add_todo(todo: TodoCreate, user_id: str = Depends(get_current_user)):
    return await create_todo(todo, user_id)

# Get all Todos
@app.get("/todos", response_model=List[TodoOut])
async def list_todos(user_id: str = Depends(get_current_user)):
    return await get_todos(user_id)

# Get single Todo
@app.get("/todos/{todo_id}", response_model=TodoOut)
async def get_single_todo(todo_id: str, user_id: str = Depends(get_current_user)):
    todo = await get_todo(todo_id, user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Update Todo
@app.put("/todos/{todo_id}", response_model=TodoOut)
async def update_single_todo(todo_id: str, data: TodoCreate, user_id: str = Depends(get_current_user)):
    todo = await update_todo(todo_id, data.dict(), user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Delete Todo
@app.delete("/todos/{todo_id}")
async def delete_single_todo(todo_id: str, user_id: str = Depends(get_current_user)):
    return await delete_todo(todo_id, user_id)
