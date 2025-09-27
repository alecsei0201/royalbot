import discord, random, time
from discord.ext import commands
from discord import app_commands
class Rps(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="rps", description="rps command")
    async def rps(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"rps: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Rps(bot))
