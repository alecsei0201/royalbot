import discord, random, time
from discord.ext import commands
from discord import app_commands
class Binary(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="binary", description="binary command")
    async def binary(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"binary: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Binary(bot))
