import discord, random, time
from discord.ext import commands
from discord import app_commands
class Snipe(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="snipe", description="snipe command")
    async def snipe(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"snipe: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Snipe(bot))
