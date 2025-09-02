import discord, random, time
from discord.ext import commands
from discord import app_commands
class Calc(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="calc", description="calc command")
    async def calc(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"calc: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Calc(bot))
