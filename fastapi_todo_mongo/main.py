from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from contextlib import asynccontextmanager
import logging

from models import UserCreate, UserOut, TodoCreate, TodoOut, Token
from crud import create_user, authenticate_user, create_todo, get_todos, get_todo, update_todo, delete_todo
from auth import create_access_token, decode_access_token
from database import get_users_collection, get_todos_collection

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    from database import init_db
    await init_db()
    yield
    # Shutdown (if needed)

app = FastAPI(title="FastAPI Todo App with MongoDB", lifespan=lifespan) 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Allow React frontend
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# JWT auth dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user_id

# -------------------------
# Health check
# -------------------------
@app.get("/health")
async def health_check():
    if get_users_collection() is not None and get_todos_collection() is not None:
        return {"status": "healthy", "database": "connected"}
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database not connected")

# -------------------------
# Register
# -------------------------
@app.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    if get_users_collection() is None:
        raise HTTPException(status_code=503, detail="Database not available")

    new_user = await create_user(user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return new_user

# -------------------------
# Login
# -------------------------
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if get_users_collection() is None:
        raise HTTPException(status_code=503, detail="Database not available")

    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": str(user["id"])})
    return {"access_token": access_token, "token_type": "bearer"}

# Alias for frontend
@app.post("/login", response_model=Token)
async def login_alias(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(form_data)

# -------------------------
# Todo CRUD
# -------------------------
@app.post("/todos", response_model=TodoOut)
async def add_todo(todo: TodoCreate, user_id: str = Depends(get_current_user)):
    if get_todos_collection() is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await create_todo(todo, user_id)

@app.get("/todos", response_model=List[TodoOut])
async def list_todos(user_id: str = Depends(get_current_user)):
    if get_todos_collection() is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await get_todos(user_id)

@app.get("/todos/{todo_id}", response_model=TodoOut)
async def get_single_todo(todo_id: str, user_id: str = Depends(get_current_user)):
    if get_todos_collection() is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    todo = await get_todo(todo_id, user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoOut)
async def update_single_todo(todo_id: str, data: TodoCreate, user_id: str = Depends(get_current_user)):
    if get_todos_collection() is None:
        raise HTTPException(status_code=503, detail="Database not available")

    todo = await update_todo(todo_id, data.dict(), user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}")
async def delete_single_todo(todo_id: str, user_id: str = Depends(get_current_user)):
    if get_todos_collection() is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await delete_todo(todo_id, user_id)
