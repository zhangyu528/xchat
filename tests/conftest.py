# tests/conftest.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
import os

from dotenv import load_dotenv
# 加载测试数据库配置
load_dotenv(".env.test")
# 读取测试数据库连接字符串（用于测试数据库环境）
TEST_DATABASE_URL = os.getenv("DATABASE_URL")

# 创建测试数据库引擎，确保不会对正式数据库造成影响
# 通常使用 SQLite 或测试专用 PostgreSQL 实例
test_engine = create_engine(TEST_DATABASE_URL)
# 使用测试数据库引擎创建 session 工厂
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# 设置测试数据库的表结构（测试运行前创建，运行后销毁）
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # 确保测试环境干净，删除所有旧的表
    Base.metadata.drop_all(bind=test_engine)
    # 创建所有模型对应的表
    Base.metadata.create_all(bind=test_engine)
    yield  # 测试用例执行时暂停在这里，测试完成后继续执行下面的清理逻辑
    # 清理测试数据，避免影响后续测试或开发
    Base.metadata.drop_all(bind=test_engine)


# 提供测试数据库的依赖项（替代应用中原始的 get_db）
@pytest.fixture()
def override_get_db():
    def _override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    return _override_get_db

# 自动将测试用的 get_db 覆盖到 FastAPI 应用中
# 所有依赖 get_db 的接口都会使用 override_get_db
@pytest.fixture(autouse=True)
def apply_override(override_get_db):
    app.dependency_overrides[get_db] = override_get_db

# 提供测试客户端，用于模拟 HTTP 请求调用接口
@pytest.fixture()
def client():
    return TestClient(app)
