import discord, random, time
from discord.ext import commands
from discord import app_commands
class Userid(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="userid", description="userid command")
    async def userid(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"userid: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Userid(bot))
