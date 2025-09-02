import discord, random, time
from discord.ext import commands
from discord import app_commands
class Coinflip(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="coinflip", description="coinflip command")
    async def coinflip(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"coinflip: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Coinflip(bot))
