from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings

class Settings(BaseSettings):
    authjwt_secret_key: str

    class Config:
        env_file = ".env"  # 自动读取 .env 文件

@AuthJWT.load_config
def get_config():
    return Settings()