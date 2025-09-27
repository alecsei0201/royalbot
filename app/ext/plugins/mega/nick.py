from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class Nickname(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="nick", description="Сменить никнейм участнику.")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def nick(self, interaction: Interaction, member: discord.Member, nickname: str | None = None):
        await member.edit(nick=nickname)
        await interaction.response.send_message(f"✏️ Установлен ник {member.mention}: `{nickname or 'сброшен'}`")


async def setup(bot: commands.Bot):
    await bot.add_cog(Nickname(bot))
