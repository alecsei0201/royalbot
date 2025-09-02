from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="avatar", description="Аватар пользователя.")
    async def avatar(self, interaction: Interaction, user: discord.User | None = None):
        user = user or interaction.user
        embed = Embed(title=f"👤 Аватар — {user}", color=COLOR)
        embed.set_image(url=user.display_avatar.replace(size=512).url)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Avatar(bot))
