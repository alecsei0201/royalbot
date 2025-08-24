from __future__ import annotations
import os
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv, find_dotenv

# --- Robust .env loading ---
# We try multiple likely locations so the bot picks up .env
# even if you run from a parent folder or a different working dir.
def _load_env_robust() -> None:
    candidates: List[Path] = []

    # 1) Current working directory
    candidates.append(Path(os.getcwd()) / ".env")

    # 2) Project root relative to this file: app/core/config.py -> project_root
    this = Path(__file__).resolve()
    for up in [2, 3, 4]:
        try:
            candidates.append(this.parents[up] / ".env")
        except IndexError:
            pass

    # 3) Use python-dotenv's search
    fd1 = find_dotenv(usecwd=True)
    if fd1:
        candidates.append(Path(fd1))
    fd2 = find_dotenv()
    if fd2:
        candidates.append(Path(fd2))

    loaded_any = False
    for p in candidates:
        if p and p.exists():
            load_dotenv(dotenv_path=str(p), override=False)
            loaded_any = True

    if not loaded_any:
        # As a last resort, call load_dotenv() to load from CWD if present
        load_dotenv(override=False)

_load_env_robust()

class Settings(BaseModel):
    token: str = Field(validation_alias="DISCORD_TOKEN")
    owner_id: int = Field(validation_alias="OWNER_ID")
    test_guild_id: int | None = Field(default=None, validation_alias="TEST_GUILD_ID")
    prefix: str = Field(default="!", validation_alias="BOT_PREFIX")
    db_path: str = Field(default=os.getenv("DB_PATH", "/tmp/royalbot.db"))
    log_level: str = Field(default=os.getenv("LOG_LEVEL", "INFO"))

    # Feature flags
    enable_automod: bool = Field(default=os.getenv("ENABLE_AUTOMOD", "true").lower() == "true")
    enable_leveling: bool = Field(default=os.getenv("ENABLE_LEVELING", "true").lower() == "true")
    enable_tickets: bool = Field(default=os.getenv("ENABLE_TICKETS", "true").lower() == "true")
    enable_welcome: bool = Field(default=os.getenv("ENABLE_WELCOME", "true").lower() == "true")
    enable_music: bool = Field(default=os.getenv("ENABLE_MUSIC", "false").lower() == "true")

    # Welcome
    welcome_channel_id: int | None = Field(default=None, validation_alias="WELCOME_CHANNEL_ID")
    welcome_message: str = Field(default=os.getenv("WELCOME_MESSAGE", "Добро пожаловать, {member.mention}!"))

    # Lavalink
    lavalink_url: str | None = Field(default=None, validation_alias="LAVALINK_URL")
    lavalink_password: str | None = Field(default=None, validation_alias="LAVALINK_PASSWORD")
    lavalink_secure: bool = Field(default=os.getenv("LAVALINK_SECURE", "false").lower() == "true")

    # Premium gating
    premium_role_id: int | None = Field(default=None, validation_alias="PREMIUM_ROLE_ID")
    premium_guilds: list[int] = Field(default_factory=list, validation_alias="PREMIUM_GUILDS")

    # External APIs (optional)
    youtube_api_key: str | None = Field(default=None, validation_alias="YOUTUBE_API_KEY")
    spotify_client_id: str | None = Field(default=None, validation_alias="SPOTIFY_CLIENT_ID")
    spotify_client_secret: str | None = Field(default=None, validation_alias="SPOTIFY_CLIENT_SECRET")
    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    elevenlabs_api_key: str | None = Field(default=None, validation_alias="ELEVENLABS_API_KEY")
    stripe_api_key: str | None = Field(default=None, validation_alias="STRIPE_API_KEY")
    topgg_token: str | None = Field(default=None, validation_alias="TOPGG_TOKEN")
    steam_api_key: str | None = Field(default=None, validation_alias="STEAM_WEB_API_KEY")
    twitch_client_id: str | None = Field(default=None, validation_alias="TWITCH_CLIENT_ID")
    twitch_client_secret: str | None = Field(default=None, validation_alias="TWITCH_CLIENT_SECRET")

    sentry_dsn: str | None = Field(default=None, validation_alias="SENTRY_DSN")

    def is_premium_guild(self, guild_id: int | None) -> bool:
        if guild_id is None:
            return False
        return guild_id in set(self.premium_guilds)

def get_settings() -> Settings:
    raw_premium = os.getenv("PREMIUM_GUILDS", "")
    premium_list = [int(x.strip()) for x in raw_premium.split(",") if x.strip().isdigit()]
    try:
        settings = Settings(premium_guilds=premium_list)
    except ValidationError as e:
        raise RuntimeError(
            "Config validation error: "
            f"{e}\n"
            "Подсказка: создайте файл .env в КОРНЕ проекта и задайте минимум:\n"
            "DISCORD_TOKEN=...\n"
            "OWNER_ID=...\n"
            "Либо установите переменные окружения в PowerShell:\n"
            '$env:DISCORD_TOKEN="..." ; $env:OWNER_ID="..."\n'
            "Если проект в вложенной папке — запустите команду из той папки или переместите .env в корень."
        ) from e
    return settings