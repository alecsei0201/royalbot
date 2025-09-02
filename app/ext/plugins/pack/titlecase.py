import discord, random, time
from discord.ext import commands
from discord import app_commands
class Titlecase(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="titlecase", description="titlecase command")
    async def titlecase(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"titlecase: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Titlecase(bot))
