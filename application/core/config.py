from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn, SecretStr


class RunAppConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 3535


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 10


class AuthConfig(BaseModel):
    secret_key: SecretStr
    algorithm: str
    access_token_expire_minutes = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APPLICATION__"
    )

    run: RunAppConfig = RunAppConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    auth: AuthConfig = AuthConfig()


settings = Settings()
