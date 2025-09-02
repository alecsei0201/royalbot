import discord, random, time
from discord.ext import commands
from discord import app_commands
class RegexTest(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="regex_test", description="regex_test command")
    async def regex_test(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"regex_test: " + (text or "ok"))
async def setup(bot): await bot.add_cog(RegexTest(bot))
