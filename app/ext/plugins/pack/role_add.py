import discord, random, time
from discord.ext import commands
from discord import app_commands
class RoleAdd(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="role_add", description="role_add command")
    async def role_add(self, it: discord.Interaction, text: str | None = None):
        await it.response.send_message(f"role_add: " + (text or "ok"))
async def setup(bot): await bot.add_cog(RoleAdd(bot))
