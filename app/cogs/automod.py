from __future__ import annotations
import logging, discord
from discord.ext import commands
from ..core.config import get_settings

log = logging.getLogger(__name__)
BAD_WORDS = {"badword1", "badword2"}  # пример; замените списком/моделью

class AutoMod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.enabled = get_settings().enable_automod

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not self.enabled or msg.author.bot or not msg.guild:
            return
        content = msg.content.lower()
        if any(b in content for b in BAD_WORDS):
            try:
                await msg.delete()
                await msg.channel.send(f"{msg.author.mention}, пожалуйста, без нарушений.", delete_after=5)
            except discord.Forbidden:
                log.warning("Нет прав на удаление сообщения.")

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoMod(bot))
