import discord, random, time
from discord.ext import commands
from discord import app_commands
class ReactionrolesStub(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="reactionroles", description="reactionroles command")
    async def reactionroles(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"reactionroles: " + (text or "ok"))
async def setup(bot): await bot.add_cog(ReactionrolesStub(bot))
