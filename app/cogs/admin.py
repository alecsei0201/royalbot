from typing import Literal
import discord
from discord import app_commands
from discord.ext import commands
from app.core.config import get_settings

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ... здесь остальные команды админа ...

    @app_commands.command(name="sync", description="Синхронизировать слэш-команды")
    async def sync_slash(
        self,
        interaction: discord.Interaction,
        scope: Literal["guild", "global"] = "guild",
    ):
        s = get_settings()
        # только админ сервера или владелец бота
        is_owner = interaction.user.id == s.owner_id
        is_admin = getattr(interaction.user.guild_permissions, "administrator", False)
        if not (is_owner or is_admin):
            return await interaction.response.send_message(
                "Нужны права администратора (или владелец бота).",
                ephemeral=True,
            )

        try:
            if scope == "guild" or s.test_guild_id:
                guild_id = s.test_guild_id or interaction.guild_id
                gobj = discord.Object(id=guild_id)
                # чистим возможные «застрявшие» команды и синкаем заново
                self.bot.tree.clear_commands(guild=gobj)
                self.bot.tree.copy_global_to(guild=gobj)
                synced = await self.bot.tree.sync(guild=gobj)
                await interaction.response.send_message(
                    f"Синкнуты {len(synced)} команд для сервера {guild_id}.",
                    ephemeral=True,
                )
            else:
                synced = await self.bot.tree.sync()
                await interaction.response.send_message(
                    f"Глобально синкнуто {len(synced)} команд. "
                    f"Появятся у всех в течение ~часа.",
                    ephemeral=True,
                )
        except Exception as e:
            await interaction.response.send_message(f"Ошибка синка: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))