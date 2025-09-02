import discord, random, time
from discord.ext import commands
from discord import app_commands
class TranslateStub(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="translate", description="translate command")
    async def translate(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"translate: " + (text or "ok"))
async def setup(bot): await bot.add_cog(TranslateStub(bot))
