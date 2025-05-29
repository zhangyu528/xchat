from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str