from __future__ import annotations
import logging, discord
from discord.ext import commands
from ..core.config import get_settings

log = logging.getLogger(__name__)

class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        s = get_settings()
        self.enabled = s.enable_welcome
        self.channel_id = s.welcome_channel_id
        self.template = s.welcome_message

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not self.enabled or not self.channel_id:
            return
        channel = member.guild.get_channel(self.channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            text = self.template.replace("{member.mention}", member.mention)
            await channel.send(text)

async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
