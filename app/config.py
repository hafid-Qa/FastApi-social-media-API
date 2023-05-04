from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_type: str
    database_driver: str
    database_hostname: str
    database_port: int
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    @property
    def sqlalchemy_database_uri(self) -> str:
        return f"{self.database_type}+{self.database_driver}://{self.database_username}:{self.database_password}@{self.database_hostname}:{self.database_port}/{self.database_name}"

    @property
    def sqlalchemy_database_uri_test(self) -> str:
        return f"{self.database_type}+{self.database_driver}://{self.database_username}:{self.database_password}@{self.database_hostname}_test:{self.database_port}/{self.database_name}_test"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()

settings = get_settings()
