import discord, random
from discord.ext import commands
from discord import app_commands
class Utilities(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="ping", description="Пинг")
    async def ping(self, it: discord.Interaction):
        await it.response.send_message(f"Pong! {round(self.bot.latency*1000)}ms")
    @app_commands.command(name="avatar", description="Аватар пользователя")
    async def avatar(self, it: discord.Interaction, member: discord.Member|None=None):
        m=member or it.user; await it.response.send_message(m.display_avatar.url)
    @app_commands.command(name="dice", description="Бросить кубик")
    async def dice(self, it: discord.Interaction):
        await it.response.send_message(f"🎲 {random.randint(1,6)}")
async def setup(bot): await bot.add_cog(Utilities(bot))
