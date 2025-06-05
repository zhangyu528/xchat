
# 安装依赖
poetry install

# 以开发模式启动（自动重载）
poetry run uvicorn app.main:app_sio --reload

# 以生产模式启动
poetry run uvicorn app.main:app_sio --host 0.0.0.0 --port 5002 --workers 4 --log-level error

# 初始化迁移（只需执行一次）
poetry run alembic init migrations

# 生成迁移脚本
poetry run alembic revision --autogenerate -m "描述信息"

# 应用迁移到数据库
poetry run alembic upgrade head

# 运行测试
poetry run pytest