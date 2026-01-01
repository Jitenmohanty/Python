from fastapi import APIRouter, Header, HTTPException
from models.user_model import UserModel, UpdateUser
from schemas.auth_schema import LoginSchema
from controller.user_controller import (
    register_user, login_user, get_profile, update_profile
)
from utils.jwt_handler import verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user: UserModel):
    res = register_user(user)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@router.post("/login")
def login(data: LoginSchema):
    res = login_user(data.email, data.password)
    if "error" in res:
        raise HTTPException(status_code=401, detail=res["error"])
    return res

@router.get("/profile")
def profile(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1] if Authorization else None
    if not token:
        raise HTTPException(401, "Authorization token required")
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(401, "Invalid or expired token")

    return get_profile(user_id)

@router.put("/update")
def update(data: UpdateUser, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1] if Authorization else None
    if not token:
        raise HTTPException(401, "Authorization token required")
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(401, "Invalid or expired token")

    return update_profile(user_id, data)
