from __future__ import annotations
import os
from pathlib import Path
from typing import List
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv

def _load_env_robust() -> None:
    # Локально подхватываем .env, на Fly это не мешает secrets
    candidates: List[Path] = [Path(os.getcwd()) / ".env"]
    this = Path(__file__).resolve()
    for up in [2, 3, 4]:
        try:
            candidates.append(this.parents[up] / ".env")
        except IndexError:
            pass
    for fd in [find_dotenv(usecwd=True), find_dotenv()]:
        if fd:
            candidates.append(Path(fd))
    for p in candidates:
        if p and p.exists():
            load_dotenv(dotenv_path=str(p), override=False)
            break

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", case_sensitive=True)

    # Обязательные
    token: str = Field(alias="DISCORD_TOKEN")
    owner_id: int = Field(alias="OWNER_ID")

    # Опциональные числовые: допускаем '', превращаем в None
    test_guild_id: int | None = Field(default=None, alias="TEST_GUILD_ID")
    welcome_channel_id: int | None = Field(default=None, alias="WELCOME_CHANNEL_ID")
    suggestions_channel_id: int | None = Field(default=None, alias="SUGGESTIONS_CHANNEL_ID")
    starboard_channel_id: int | None = Field(default=None, alias="STARBOARD_CHANNEL_ID")
    autorole_id: int | None = Field(default=None, alias="AUTOROLE_ID")
    muted_role_id: int | None = Field(default=None, alias="MUTED_ROLE_ID")

    # Прочее
    prefix: str = Field(default="!", alias="BOT_PREFIX")
    db_path: str = Field(default=os.getenv("DB_PATH", "/data/royalbot.db"), alias="DB_PATH")
    log_level: str = Field(default=os.getenv("LOG_LEVEL", "INFO"), alias="LOG_LEVEL")

    enable_automod: bool = Field(default=True, alias="ENABLE_AUTOMOD")
    enable_leveling: bool = Field(default=True, alias="ENABLE_LEVELING")
    enable_tickets: bool = Field(default=True, alias="ENABLE_TICKETS")
    enable_welcome: bool = Field(default=True, alias="ENABLE_WELCOME")
    enable_music: bool = Field(default=False, alias="ENABLE_MUSIC")

    @field_validator(
        "test_guild_id", "welcome_channel_id", "suggestions_channel_id",
        "starboard_channel_id", "autorole_id", "muted_role_id",
        mode="before",
    )
    @classmethod
    def _empty_str_to_none_for_ints(cls, v):
        if v is None:
            return None
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

def get_settings() -> Settings:
    _load_env_robust()
    try:
        return Settings()
    except ValidationError as e:
        # Покажем реальные ошибки (какое поле, что не так)
        raise RuntimeError(f"Config validation error: {e}") from e