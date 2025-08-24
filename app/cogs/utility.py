from __future__ import annotations
import platform, discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(description="Информация о сервере")
    async def serverinfo(self, ctx: commands.Context):
        g = ctx.guild
        await ctx.reply(f"Сервер: **{g.name}**, участников: {g.member_count}")

    @commands.hybrid_command(description="Сказать от лица бота")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx: commands.Context, *, text: str):
        await ctx.message.delete()
        await ctx.send(text)

    @commands.hybrid_command(description="Инфо о системе")
    async def sysinfo(self, ctx: commands.Context):
        await ctx.reply(f"Python: {platform.python_version()} | Latency: {round(self.bot.latency*1000)}ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
