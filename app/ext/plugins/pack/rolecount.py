import discord, random, time
from discord.ext import commands
from discord import app_commands
class Rolecount(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="rolecount", description="rolecount command")
    async def rolecount(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"rolecount: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Rolecount(bot))
