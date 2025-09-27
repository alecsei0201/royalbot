import discord, random, time
from discord.ext import commands
from discord import app_commands
class Math(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="math", description="math command")
    async def math(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"math: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Math(bot))
