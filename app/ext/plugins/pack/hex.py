import discord, random, time
from discord.ext import commands
from discord import app_commands
class Hex(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="hex", description="hex command")
    async def hex(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"hex: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Hex(bot))
