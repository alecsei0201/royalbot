from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="serverinfo", description="Информация о сервере.")
    async def serverinfo(self, interaction: Interaction):
        g = interaction.guild
        if not g:
            return await interaction.response.send_message("Только на сервере.", ephemeral=True)
        embed = Embed(title=f"ℹ️ {g.name}", color=COLOR)
        embed.add_field(name="Участников", value=str(g.member_count))
        embed.add_field(name="Создан", value=discord.utils.format_dt(g.created_at, style='D'))
        if g.icon: embed.set_thumbnail(url=g.icon.url)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfo(bot))
