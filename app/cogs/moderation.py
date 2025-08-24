from __future__ import annotations
import logging
from discord.ext import commands
import discord
from ..core.db import DB

log = logging.getLogger(__name__)

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot, db: DB):
        self.bot = bot
        self.db = db

    @commands.hybrid_command(description="Выдать предупреждение пользователю")
    @commands.has_guild_permissions(moderate_members=True)
    async def warn(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Не указано"):
        await self.db.conn.execute(
            "INSERT INTO warns (guild_id, user_id, mod_id, reason) VALUES (?, ?, ?, ?)",
            (ctx.guild.id, member.id, ctx.author.id, reason),
        )
        await self.db.conn.commit()
        await ctx.reply(f"Выдано предупреждение {member.mention}: {reason}")

    @commands.hybrid_command(description="Список предупреждений пользователя")
    @commands.has_guild_permissions(moderate_members=True)
    async def warns(self, ctx: commands.Context, member: discord.Member):
        async with self.db.conn.execute(
            "SELECT reason, ts FROM warns WHERE guild_id=? AND user_id=? ORDER BY ts DESC",
            (ctx.guild.id, member.id)
        ) as cur:
            rows = await cur.fetchall()
        if not rows:
            await ctx.reply("Нет предупреждений.")
            return
        text = "\n".join(f"- {ts}: {reason}" for (reason, ts) in rows)
        await ctx.reply(f"Предупреждения {member.mention}:\n{text}")

    @commands.hybrid_command(description="Кикнуть пользователя")
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await member.kick(reason=reason)
        await ctx.reply(f"{member} кикнут.")

    @commands.hybrid_command(description="Забанить пользователя")
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await member.ban(reason=reason, delete_message_days=0)
        await ctx.reply(f"{member} забанен.")

async def setup(bot: commands.Bot):
    db: DB = bot.db  # type: ignore[attr-defined]
    await bot.add_cog(Moderation(bot, db))
