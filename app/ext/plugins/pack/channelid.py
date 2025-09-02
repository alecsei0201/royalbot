import discord, random, time
from discord.ext import commands
from discord import app_commands
class Channelid(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="channelid", description="channelid command")
    async def channelid(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"channelid: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Channelid(bot))
