import os

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    title: str = Field(default="Python Project Template", validation_alias="app.title")
    profile: str = Field(default="default", validation_alias="app.profile")
    log_level: str = Field(default="INFO", validation_alias="app.log.level")

    class Config:
        env_file = f".env.{os.getenv("PROFILE", "")}"
