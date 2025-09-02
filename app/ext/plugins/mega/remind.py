from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class Remind(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="remindme", description="Напомнить через N минут.")
    async def remindme(self, interaction: Interaction, minutes: int, текст: str):
        await interaction.response.send_message(f"⏰ Напомню через {minutes} мин.", ephemeral=True)
        await asyncio.sleep(max(0, minutes*60))
        try:
            await interaction.followup.send(f"⏰ Напоминание: {текст}", ephemeral=True)
        except Exception:
            pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Remind(bot))
