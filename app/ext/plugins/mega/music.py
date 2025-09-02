from __future__ import annotations
import asyncio, functools
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import yt_dlp

YTDL_OPTS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
}
FFMPEG_OPTS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

class MusicQueue:
    def __init__(self):
        self.q: list[tuple[str, str]] = []
    def add(self, t,u): self.q.append((t,u))
    def pop(self): return self.q.pop(0) if self.q else None
    def clear(self): self.q.clear()
    def __len__(self): return len(self.q)
    def view(self): return "\\n".join(f"{i+1}. {t}" for i,(t,_) in enumerate(self.q)) or "пусто"

class Music(commands.Cog):
    def __init__(self, bot): self.bot = bot; self.queues: dict[int, MusicQueue] = {}

    def get_q(self, gid: int): self.queues.setdefault(gid, MusicQueue()); return self.queues[gid]

    async def ensure_voice(self, it: Interaction):
        if not it.guild or not isinstance(it.user, discord.Member):
            raise RuntimeError("Только на сервере.")
        if not it.user.voice or not it.user.voice.channel:
            raise RuntimeError("Зайдите в голосовой канал.")
        vc = it.guild.voice_client
        if vc and vc.channel != it.user.voice.channel:
            await vc.move_to(it.user.voice.channel)
        elif not vc:
            vc = await it.user.voice.channel.connect()  # type: ignore
        return vc

    def ytdl_extract(self, query: str):
        with yt_dlp.YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info: info = info['entries'][0]
            return info.get('title') or 'unknown', info['url']

    async def start_playback(self, g: discord.Guild, vc: discord.VoiceClient):
        q = self.get_q(g.id)
        while True:
            item = q.pop()
            if not item: break
            title, url = item
            src = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTS)
            vc.play(src)
            while vc.is_playing() or vc.is_paused():
                await asyncio.sleep(1)
        await vc.disconnect()

    @app_commands.command(name="music_play", description="Проиграть трек/поиск YouTube (без ключей).")
    async def music_play(self, it: Interaction, query: str):
        await it.response.defer()
        try:
            vc = await self.ensure_voice(it)
        except Exception as e:
            return await it.followup.send(str(e), ephemeral=True)
        loop = asyncio.get_running_loop()
        title, url = await loop.run_in_executor(None, functools.partial(self.ytdl_extract, query))
        q = self.get_q(it.guild_id)  # type: ignore
        q.add(title, url)
        await it.followup.send(embed=Embed(title="➕ В очередь", description=title, color=0x2b2d31))
        if not vc.is_playing():
            await self.start_playback(it.guild, vc)  # type: ignore

    @app_commands.command(name="music_skip", description="Пропустить трек.")
    async def music_skip(self, it: Interaction):
        vc = it.guild.voice_client if it.guild else None
        if not vc: return await it.response.send_message("Не воспроизводится.", ephemeral=True)
        vc.stop(); await it.response.send_message("⏭️ Пропуск.")

    @app_commands.command(name="music_pause", description="Пауза.")
    async def music_pause(self, it: Interaction):
        vc = it.guild.voice_client if it.guild else None
        if not vc: return await it.response.send_message("Не воспроизводится.", ephemeral=True)
        vc.pause(); await it.response.send_message("⏸️ Пауза.")

    @app_commands.command(name="music_resume", description="Продолжить.")
    async def music_resume(self, it: Interaction):
        vc = it.guild.voice_client if it.guild else None
        if not vc: return await it.response.send_message("Не воспроизводится.", ephemeral=True)
        vc.resume(); await it.response.send_message("▶️ Продолжить.")

    @app_commands.command(name="music_queue", description="Очередь.")
    async def music_queue(self, it: Interaction):
        q = self.get_q(it.guild_id)  # type: ignore
        await it.response.send_message(embed=Embed(title="🎶 Очередь", description=q.view(), color=0x2b2d31), ephemeral=True)

    @app_commands.command(name="music_stop", description="Остановить и выйти.")
    async def music_stop(self, it: Interaction):
        vc = it.guild.voice_client if it.guild else None
        if not vc: return await it.response.send_message("Не воспроизводится.", ephemeral=True)
        self.get_q(it.guild_id).clear()  # type: ignore
        vc.stop(); await vc.disconnect()
        await it.response.send_message("⏹️ Остановлено.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
