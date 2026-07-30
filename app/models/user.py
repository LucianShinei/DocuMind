from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime