import discord, random, time
from discord.ext import commands
from discord import app_commands
class Whois(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="whois", description="whois command")
    async def whois(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"whois: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Whois(bot))
