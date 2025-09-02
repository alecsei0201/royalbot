import discord, random, time
from discord.ext import commands
from discord import app_commands
class Len(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="len", description="len command")
    async def len(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"len: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Len(bot))
