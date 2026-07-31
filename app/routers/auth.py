from fastapi import APIRouter, HTTPException

from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import register_user, login_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
async def register(user: UserCreate):
    try:
        return await register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    try:
        return await login_user(
                form_data.username,
                form_data.password,
            )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))