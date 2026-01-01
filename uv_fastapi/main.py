from fastapi import FastAPI
from routes.todo_routes import router as todo_router
from routes.user_routes import router as user_router

app = FastAPI()

app.include_router(todo_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "API running with Auth + Todo"}
