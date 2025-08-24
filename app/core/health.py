from __future__ import annotations
import os, sys, discord
from .config import get_settings

def self_check() -> dict:
    s = get_settings()
    checks = {
        "python_version": sys.version,
        "discord_py": discord.__version__,
        "has_token": bool(s.token),
        "db_path": s.db_path,
        "feature_flags": {
            "automod": s.enable_automod,
            "leveling": s.enable_leveling,
            "tickets": s.enable_tickets,
            "welcome": s.enable_welcome,
            "music": s.enable_music,
        },
        "lavalink_configured": bool(s.lavalink_url and s.lavalink_password),
        "premium_role_id": s.premium_role_id,
        "premium_guilds": s.premium_guilds,
    }
    return checks
