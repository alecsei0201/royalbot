from __future__ import annotations
import random, discord
from discord.ext import commands
from ..core.db import DB
from ..core.config import get_settings

class Leveling(commands.Cog):
    def __init__(self, bot: commands.Bot, db: DB):
        self.bot = bot
        self.db = db
        self.enabled = get_settings().enable_leveling

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.enabled or message.author.bot or not message.guild:
            return
        xp_gain = random.randint(1, 5)
        await self.db.conn.execute(
            """
            INSERT INTO levels (guild_id, user_id, xp, level) VALUES (?, ?, ?, 0)
            ON CONFLICT(guild_id, user_id) DO UPDATE SET xp = xp + excluded.xp
            """,
            (message.guild.id, message.author.id, xp_gain)
        )
        await self.db.conn.commit()

    @commands.hybrid_command(description="Ваш уровень/XP")
    async def rank(self, ctx: commands.Context, member: discord.Member | None = None):
        member = member or ctx.author
        async with self.db.conn.execute(
            "SELECT xp, level FROM levels WHERE guild_id=? AND user_id=?",
            (ctx.guild.id, member.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await ctx.reply("Ещё нет данных.")
            return
        xp, level = row
        await ctx.reply(f"{member.mention} — XP: {xp}, LVL: {level}")

async def setup(bot: commands.Bot):
    db: DB = bot.db  # type: ignore
    await bot.add_cog(Leveling(bot, db))
