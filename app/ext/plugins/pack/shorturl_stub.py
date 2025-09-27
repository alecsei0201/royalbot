import discord, random, time
from discord.ext import commands
from discord import app_commands
class ShorturlStub(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="shorturl", description="shorturl command")
    async def shorturl(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"shorturl: " + (text or "ok"))
async def setup(bot): await bot.add_cog(ShorturlStub(bot))
