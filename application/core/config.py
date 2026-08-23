from pydantic_settings import BaseSettings
from pydantic import BaseModel, PostgresDsn


class RunAppConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 3535


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False,
    echo_pool: bool = False,
    pool_size: int = 10,
    max_overflow: int = 10


class Settings(BaseSettings):
    run: RunAppConfig = RunAppConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
