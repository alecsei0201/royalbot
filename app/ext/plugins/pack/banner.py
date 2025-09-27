import discord, random, time
from discord.ext import commands
from discord import app_commands
class Banner(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="banner", description="banner command")
    async def banner(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"banner: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Banner(bot))
