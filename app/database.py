# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 加载 .env 环境变量（可选）
load_dotenv()

# 从环境变量中读取数据库连接字符串
DATABASE_URL = os.getenv("SYNC_DATABASE_URL")

# 创建数据库引擎（同步版本）
engine = create_engine(DATABASE_URL, echo=True)

# 创建数据库会话工厂（SessionLocal 是一个类，用来创建 Session 实例）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建所有模型的基类
Base = declarative_base()

# FastAPI 依赖项：为每个请求提供一个新的数据库会话，并在请求结束后关闭
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
