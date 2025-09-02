import discord, random, time
from discord.ext import commands
from discord import app_commands
class Lower(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="lower", description="lower command")
    async def lower(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"lower: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Lower(bot))
