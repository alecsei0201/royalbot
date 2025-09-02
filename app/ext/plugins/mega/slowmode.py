from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class Slowmode(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="slowmode", description="Включить slowmode в секундах (0 чтобы снять).")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: Interaction, seconds: int):
        ch = interaction.channel
        if not isinstance(ch, discord.TextChannel):
            return await interaction.response.send_message("Только текстовый канал.", ephemeral=True)
        await ch.edit(slowmode_delay=max(0, min(21600, seconds)))
        await interaction.response.send_message(f"🐢 Slowmode: {seconds}s")


async def setup(bot: commands.Bot):
    await bot.add_cog(Slowmode(bot))
