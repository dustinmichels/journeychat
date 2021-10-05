from typing import List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        # "http://localhost.tiangolo.com",
        # "https://localhost.tiangolo.com",
        # "http://localhost",
        # "http://localhost:8080",
        # "http://localhost:8002",
        "http://localhost:3000"
    ]

    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///example.db"
    FIRST_SUPERUSER: EmailStr = "admin@journeychat.com"
    FIRST_SUPERUSER_USERNAME: str = "admin"
    FIRST_SUPERUSER_PW: str = "admin"

    class Config:
        case_sensitive = True


settings = Settings()
