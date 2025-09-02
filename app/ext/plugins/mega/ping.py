from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="ping", description="Показать задержку бота.")
    async def ping(self, interaction: Interaction):
        await interaction.response.defer(thinking=True, ephemeral=False)
        embed = Embed(title="🏓 Pong!", description=f"Latency: **{round(self.bot.latency*1000)} ms**", color=COLOR)
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
