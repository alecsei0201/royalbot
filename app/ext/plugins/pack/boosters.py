import discord, random, time
from discord.ext import commands
from discord import app_commands
class Boosters(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="boosters", description="boosters command")
    async def boosters(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"boosters: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Boosters(bot))
