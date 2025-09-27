import discord, random, time
from discord.ext import commands
from discord import app_commands
class Invite(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="invite", description="invite command")
    async def invite(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"invite: " + (text or "ok"))
async def setup(bot): await bot.add_cog(Invite(bot))
