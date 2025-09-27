from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class Lock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="lock", description="Закрыть канал для @everyone.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: Interaction, reason: str | None = None):
        ch = interaction.channel
        assert isinstance(ch, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel))
        overwrites = ch.overwrites_for(interaction.guild.default_role)  # type: ignore
        overwrites.send_messages = False
        await ch.set_permissions(interaction.guild.default_role, overwrite=overwrites)  # type: ignore
        await interaction.response.send_message(f"🔒 Канал закрыт. {('Причина: '+reason) if reason else ''}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Lock(bot))
