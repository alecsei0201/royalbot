from __future__ import annotations
import json, logging
from discord.ext import commands
from discord import app_commands
from ..core.checks import is_owner
from ..core.health import self_check

log = logging.getLogger(__name__)

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", with_app_command=True, description="Пинг бота")
    async def ping(self, ctx: commands.Context):
        await ctx.reply(f"Pong! {round(self.bot.latency*1000)}ms")

    @is_owner()
    @commands.hybrid_command(name="reload", with_app_command=True, description="Перезагрузить коги")
    async def reload(self, ctx: commands.Context):
        failed = []
        for ext in list(self.bot.extensions.keys()):
            try:
                await self.bot.reload_extension(ext)
            except Exception as e:
                failed.append((ext, str(e)))
        await ctx.reply("Reload complete. Failed: " + (json.dumps(failed, ensure_ascii=False) if failed else "0"))

    @is_owner()
    @commands.hybrid_command(name="sync", with_app_command=True, description="Синхронизировать слэш-команды")
    async def sync(self, ctx: commands.Context):
        try:
            synced = await self.bot.tree.sync()
            await ctx.reply(f"Синхронизировано {len(synced)} слэш-команд(ы).")
        except Exception as e:
            await ctx.reply(f"Ошибка sync: {e}")

    @commands.hybrid_command(name="diag", with_app_command=True, description="Диагностика бота")
    async def diag(self, ctx: commands.Context):
        data = self_check()
        await ctx.reply(f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```")

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
