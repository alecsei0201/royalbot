import discord, random, time
from discord.ext import commands
from discord import app_commands
class Nickname(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="nickname", description="nickname command")
    async def nickname(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"nickname: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Nickname(bot))
