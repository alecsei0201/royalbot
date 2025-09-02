import discord, random, time
from discord.ext import commands
from discord import app_commands
class Serverinfo(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="serverinfo", description="serverinfo command")
    async def serverinfo(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"serverinfo: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Serverinfo(bot))
