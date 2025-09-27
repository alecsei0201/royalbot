import discord, time
from discord.ext import commands
from discord import app_commands
AFK={}
class Afk(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="afk", description="Установить AFK статус")
    async def afk(self, it: discord.Interaction, reason: str="AFK"):
        AFK[it.user.id]=(time.time(),reason); await it.response.send_message("AFK поставлен.", ephemeral=True)
    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if m.author.id in AFK: del AFK[m.author.id]
        for u in m.mentions:
            if u.id in AFK:
                ts, r = AFK[u.id]; await m.channel.send(f"{u.mention} сейчас AFK: {r}")
async def setup(bot): await bot.add_cog(Afk(bot))
