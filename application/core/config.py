from pydantic_settings import BaseSettings
from pydantic import BaseModel

class RunAppConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 3535

class ApiPrefix(BaseModel):
    prefix: str = "/api"


class Settings(BaseSettings):
    run: RunAppConfig = RunAppConfig()
    api: ApiPrefix = ApiPrefix()

settings = Settings()