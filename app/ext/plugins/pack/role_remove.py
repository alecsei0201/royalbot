import discord, random, time
from discord.ext import commands
from discord import app_commands
class RoleRemove(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="role_remove", description="role_remove command")
    async def role_remove(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"role_remove: " + (text or "ok"))
async def setup(bot): await bot.add_cog(RoleRemove(bot))
