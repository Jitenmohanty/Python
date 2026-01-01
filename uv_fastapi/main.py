from fastapi import FastAPI, Request
from routes.todo_routes import router as todo_router
from routes.user_routes import router as user_router
import logging
import time

# Force uvicorn access logging
logging.getLogger("uvicorn.access").disabled = False
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"INFO: {request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
    return response

app.include_router(todo_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "API running with Auth + Todo"}
