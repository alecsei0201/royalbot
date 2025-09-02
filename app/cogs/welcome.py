import discord
from discord.ext import commands
from app.core.config import get_settings
class Welcome(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @commands.Cog.listener()
    async def on_member_join(self, m: discord.Member):
        s=get_settings()
        if s.welcome_channel_id:
            ch=m.guild.get_channel(s.welcome_channel_id)
            if ch: await ch.send(s.welcome_message.replace("{member.mention}", m.mention))
async def setup(bot): await bot.add_cog(Welcome(bot))
