import discord, random, time
from discord.ext import commands
from discord import app_commands
class Membercount(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="membercount", description="membercount command")
    async def membercount(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"membercount: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Membercount(bot))
