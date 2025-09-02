import discord, random, time
from discord.ext import commands
from discord import app_commands
class Quote(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="quote", description="quote command")
    async def quote(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"quote: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Quote(bot))
