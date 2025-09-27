import discord, random, time
from discord.ext import commands
from discord import app_commands
class Reverse(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="reverse", description="reverse command")
    async def reverse(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"reverse: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Reverse(bot))
