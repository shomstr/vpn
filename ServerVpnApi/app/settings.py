from __future__ import annotations

from pathlib import Path
from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())

ProjectDir = Path(__file__).parent.parent
AppDir = ProjectDir / "app"
LogDir = Path(ProjectDir) / "logs"


class ApiSettings(BaseSettings):
    rate_limit: int | float = 1


class Settings(BaseSettings):
    connection_token: str

    api: ApiSettings = ApiSettings()


settings = Settings()
