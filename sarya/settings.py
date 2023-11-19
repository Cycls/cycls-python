from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    Environment: str = "development"

settings = Settings(Environment="PRODUCTION")