import discord, random, time
from discord.ext import commands
from discord import app_commands
class WeatherStub(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="weather", description="weather command")
    async def weather(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"weather: " + (text or "ok"))
async def setup(bot): await bot.add_cog(WeatherStub(bot))
