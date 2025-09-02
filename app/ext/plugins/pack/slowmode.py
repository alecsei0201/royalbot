import discord
from discord.ext import commands
from discord import app_commands
class Slowmode(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="slowmode", description="Поставить slowmode в секундах")
    async def slowmode(self, it: discord.Interaction, seconds: int):
        await it.channel.edit(slowmode_delay=max(0,min(seconds,21600)))
        await it.response.send_message("Ок", ephemeral=True)
async def setup(bot): await bot.add_cog(Slowmode(bot))
