from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class UserInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="userinfo", description="Информация о пользователе.")
    async def userinfo(self, interaction: Interaction, user: discord.Member | None = None):
        m = user or interaction.user
        embed = Embed(title=f"{m}", description=f"ID: `{m.id}`", color=COLOR)
        embed.add_field(name="Создан", value=discord.utils.format_dt(m.created_at, style='F'))
        if isinstance(m, discord.Member):
            if m.joined_at:
                embed.add_field(name="Зашёл", value=discord.utils.format_dt(m.joined_at, style='F'))
            roles = [r.mention for r in m.roles if r.name != "@everyone"]
            embed.add_field(name="Роли", value=", ".join(roles) if roles else "нет", inline=False)
        embed.set_thumbnail(url=m.display_avatar.url)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(UserInfo(bot))
