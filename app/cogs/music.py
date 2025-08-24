from __future__ import annotations
import logging, wavelink
from discord.ext import commands
from ..core.config import get_settings

log = logging.getLogger(__name__)

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        s = get_settings()
        if not (s.lavalink_url and s.lavalink_password and s.enable_music):
            log.info("Music disabled or Lavalink not configured.")
            return
        if not wavelink.Pool.nodes:
            await wavelink.Pool.connect(
                client=self.bot,
                nodes=[
                    wavelink.Node(uri=s.lavalink_url, password=s.lavalink_password, secure=s.lavalink_secure)
                ]
            )
            log.info("Connected to Lavalink.")

    @commands.hybrid_command(description="Проиграть трек (требуется Lavalink)")
    async def play(self, ctx: commands.Context, *, query: str):
        s = get_settings()
        if not s.enable_music:
            await ctx.reply("Музыка отключена в настройках.")
            return
        if not wavelink.Pool.nodes:
            await ctx.reply("Lavalink не настроен.")
            return
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply("Зайдите в голосовой канал.")
            return
        channel = ctx.author.voice.channel
        player: wavelink.Player = await channel.connect(cls=wavelink.Player)
        track = await wavelink.Playable.search(query)
        if not track:
            await ctx.reply("Трек не найден.")
            return
        if isinstance(track, list):
            track = track[0]
        await player.play(track)
        await ctx.reply(f"▶️ Играет: {track.title}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
