import discord, random, time
from discord.ext import commands
from discord import app_commands
class TimezoneStub(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="timezone", description="timezone command")
    async def timezone(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"timezone: " + (text or "ok"))
async def setup(bot): await bot.add_cog(TimezoneStub(bot))
