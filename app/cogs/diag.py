import discord, platform, sys, json
from discord.ext import commands
from discord import app_commands
from app.core.config import get_settings
class Diag(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="diag", description="Показать состояние бота")
    async def diag(self, it: discord.Interaction):
        s=get_settings()
        data={"python": sys.version.split()[0], "platform": platform.platform(), "prefix": s.prefix, "db_path": s.db_path}
        await it.response.send_message(f"```json\n{json.dumps(data, ensure_ascii=False, indent=2)}\n```", ephemeral=True)
async def setup(bot): await bot.add_cog(Diag(bot))
