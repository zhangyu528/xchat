from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.user import UserCreate, UserOut, TokenResponse
from app.database import get_db  # 同步 get_db
from app.models.user import User
from passlib.hash import bcrypt
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

# 用户注册
@router.post("/register", response_model=UserOut, 
                        status_code=201, tags=["users"], 
                        summary="Create a new user",
                        description="Create a new user", 
                        response_description="User created successfully",
                        responses={409: {"description": "Email already registered"}})
def register_user_with_password(user: UserCreate, db: Session = Depends(get_db)):
    result = db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = bcrypt.hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 用户登录
@router.post("/login", response_model=TokenResponse, 
                        status_code=200, tags=["users"], 
                        summary="Login user",
                        description="Login user", 
                        response_description="User logged in successfully", 
                        responses={401: {"description": "Invalid credentials"}})
def login_user(user: UserCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    result = db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar_one_or_none()
    if not db_user or not bcrypt.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

     # 生成 access token
    access_token = Authorize.create_access_token(subject=db_user.email)
    return {"access_token": access_token} 


# 获取当前用户
@router.get("/me", response_model=UserOut, 
                        status_code=200, tags=["users"], 
                        summary="Get current user",
                        description="Get current user", 
                        response_description="Current user",
                        responses={401: {"description": "Invalid token"}, 404: {"description": "User not found"}})
def get_current_user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    email = Authorize.get_jwt_subject()
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user