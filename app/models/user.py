from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    current_jti = Column(String(36), nullable=True, comment="当前有效JWT的jti")

    username = Column(String, unique=True, index=True, nullable=False, comment="用户名")
    is_system_user = Column(Boolean, default=False, comment="是否为系统用户")
