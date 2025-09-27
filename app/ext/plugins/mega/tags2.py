from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class Tags2(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    tags: dict[str, str] = {}

    @app_commands.command(name="tag_set", description="Создать/обновить тег.")
    async def tag_set(self, interaction: Interaction, name: str, content: str):
        self.tags[name.lower()] = content
        await interaction.response.send_message(f"🏷️ Тег `{name}` сохранён.")

    @app_commands.command(name="tag_get", description="Показать тег.")
    async def tag_get(self, interaction: Interaction, name: str):
        content = self.tags.get(name.lower())
        if not content:
            return await interaction.response.send_message("Тег не найден.", ephemeral=True)
        await interaction.response.send_message(content)

    @app_commands.command(name="tag_list", description="Список тегов.")
    async def tag_list(self, interaction: Interaction):
        names = sorted(self.tags.keys())
        await interaction.response.send_message("Теги: " + (", ".join(f"`{n}`" for n in names) if names else "пусто"))


async def setup(bot: commands.Bot):
    await bot.add_cog(Tags2(bot))
