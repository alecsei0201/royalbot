import discord
from discord.ext import commands
from discord import app_commands
class Lockdown(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="lock", description="Закрыть канал")
    async def lock(self, it: discord.Interaction):
        ow = it.channel.overwrites_for(it.guild.default_role); ow.send_messages=False
        await it.channel.set_permissions(it.guild.default_role, overwrite=ow)
        await it.response.send_message("🔒 Закрыто.", ephemeral=True)
    @app_commands.command(name="unlock", description="Открыть канал")
    async def unlock(self, it: discord.Interaction):
        ow = it.channel.overwrites_for(it.guild.default_role); ow.send_messages=True
        await it.channel.set_permissions(it.guild.default_role, overwrite=ow)
        await it.response.send_message("🔓 Открыто.", ephemeral=True)
async def setup(bot): await bot.add_cog(Lockdown(bot))
