from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db
from sqlalchemy import select

def require_current_valid_token(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    Authorize.jwt_required()
    email = Authorize.get_jwt_subject()
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    jti = Authorize.get_raw_jwt().get("jti")
    if user.current_jti != jti:
        raise HTTPException(status_code=401, detail="Invalid token")
    # 不返回 user，不返回任何内容，只做校验