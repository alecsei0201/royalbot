from __future__ import annotations
import discord
from discord.ext import commands
from ..core.checks import is_owner

class VoiceJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @is_owner()
    @commands.hybrid_command(description="Зайти в голосовой канал для keepalive")
    async def vjoin(self, ctx: commands.Context, channel: discord.VoiceChannel):
        if ctx.voice_client:
            await ctx.voice_client.disconnect(force=True)
        await channel.connect(cls=discord.VoiceClient)
        await ctx.reply(f"Подключился к {channel.name}")

    @is_owner()
    @commands.hybrid_command(description="Выйти из голосового канала")
    async def vleave(self, ctx: commands.Context):
        if ctx.voice_client:
            await ctx.voice_client.disconnect(force=True)
            await ctx.reply("Отключился.")
        else:
            await ctx.reply("Я не в голосовом.")

async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceJoin(bot))
