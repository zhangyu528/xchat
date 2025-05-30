from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str