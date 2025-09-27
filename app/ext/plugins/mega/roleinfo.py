from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class RoleInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="roleinfo", description="Информация о роли.")
    async def roleinfo(self, interaction: Interaction, role: discord.Role):
        embed = Embed(title=f"Роль: {role.name}", color=role.color.value or COLOR)
        embed.add_field(name="ID", value=f"`{role.id}`")
        embed.add_field(name="Участников", value=str(len(role.members)))
        embed.add_field(name="Цвет", value=str(role.color))
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleInfo(bot))
