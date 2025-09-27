from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class StarboardSimple(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    star_threshold: int = 3
    star_channel_id: int | None = None

    @app_commands.command(name="starboard_set", description="Настроить starboard (канал и порог).")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def starboard_set(self, interaction: Interaction, channel: discord.TextChannel, threshold: int = 3):
        self.star_channel_id = channel.id
        self.star_threshold = max(1, threshold)
        await interaction.response.send_message(f"⭐ Starboard: {channel.mention}, порог {self.star_threshold}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != "⭐" or not self.star_channel_id:
            return
        ch = self.bot.get_channel(payload.channel_id)
        if not isinstance(ch, discord.TextChannel):
            return
        try:
            msg = await ch.fetch_message(payload.message_id)
        except Exception:
            return
        count = 0
        for r in msg.reactions:
            if str(r.emoji) == "⭐":
                count = r.count
                break
        if count >= self.star_threshold:
            star_ch = self.bot.get_channel(self.star_channel_id)
            if isinstance(star_ch, discord.TextChannel):
                e = Embed(description=msg.content or "(без текста)", color=COLOR)
                if hasattr(msg.author,'display_avatar'):
                    e.set_author(name=str(msg.author), icon_url=msg.author.display_avatar.url)  # type: ignore
                e.add_field(name="Ссылка", value=f"[Jump]({msg.jump_url})")
                await star_ch.send(embed=e)


async def setup(bot: commands.Bot):
    await bot.add_cog(StarboardSimple(bot))
