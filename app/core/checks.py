from __future__ import annotations
from typing import Callable
from discord.ext import commands
from .config import get_settings

def is_owner():
    settings = get_settings()
    async def predicate(ctx: commands.Context):
        return ctx.author.id == settings.owner_id
    return commands.check(predicate)

def premium_guild_only():
    settings = get_settings()
    async def predicate(ctx: commands.Context):
        gid = ctx.guild.id if ctx.guild else None
        return settings.is_premium_guild(gid)
    return commands.check(predicate)

def has_premium_role():
    settings = get_settings()
    async def predicate(ctx: commands.Context):
        if not ctx.guild or settings.premium_role_id is None:
            return False
        role = ctx.guild.get_role(settings.premium_role_id)
        return role in getattr(ctx.author, "roles", [])
    return commands.check(predicate)
