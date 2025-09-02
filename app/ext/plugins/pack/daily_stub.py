import discord, random, time
from discord.ext import commands
from discord import app_commands
class DailyStub(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="daily", description="daily command")
    async def daily(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"daily: " + (text or "ok"))
async def setup(bot): await bot.add_cog(DailyStub(bot))
