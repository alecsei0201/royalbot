import discord, random, time
from discord.ext import commands
from discord import app_commands
class Upper(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="upper", description="upper command")
    async def upper(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"upper: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Upper(bot))
