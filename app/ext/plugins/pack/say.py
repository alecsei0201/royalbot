import discord
from discord.ext import commands
from discord import app_commands
class Say(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="say", description="Сказать от лица бота")
    async def say(self, it: discord.Interaction, text: str):
        await it.response.send_message("✅", ephemeral=True)
        await it.channel.send(text)
async def setup(bot): await bot.add_cog(Say(bot))
