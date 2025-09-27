from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class Unlock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="unlock", description="Открыть канал для @everyone.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: Interaction):
        ch = interaction.channel
        assert isinstance(ch, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel))
        await ch.set_permissions(interaction.guild.default_role, send_messages=None)  # type: ignore
        await interaction.response.send_message("🔓 Канал открыт.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Unlock(bot))
