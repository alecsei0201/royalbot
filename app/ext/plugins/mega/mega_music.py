
import discord
from discord import app_commands, Interaction
from discord.ext import commands

# Nested music group: /mega music <subcommand>
music = app_commands.Group(name="music", description="Музыка без ключей (требуется PyNaCl + ffmpeg)")
# this group will be attached as a sub-group under /mega in setup()

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot, parent_group: app_commands.Group):
        self.bot = bot
        self.parent = parent_group
        # Attach subgroup
        # Note: in discord.py 2.x we can add a subgroup by specifying parent in add_command
        if not any(isinstance(cmd, app_commands.Group) and cmd.name == music.name for cmd in parent_group.commands):
            parent_group.add_command(music)

    @music.command(name="status", description="Проверка возможности воспроизведения")
    async def status(self, interaction: Interaction):
        try:
            import nacl  # type: ignore
            has_nacl = True
        except Exception:
            has_nacl = False
        ffmpeg_ok = discord.opus.is_loaded()
        txt = []
        txt.append(f"PyNaCl: {'✅' if has_nacl else '❌'}")
        txt.append(f"Opus/FFmpeg: {'✅' if ffmpeg_ok else '❌'}")
        if not has_nacl or not ffmpeg_ok:
            txt.append("Установите зависимости, иначе музыка не работает.")
        await interaction.response.send_message("\n".join(txt), ephemeral=True)

async def setup(bot: commands.Bot):
    # Find the /mega group created by mega_core and attach music subgroup under it
    mega = None
    for cmd in bot.tree.get_commands():
        if isinstance(cmd, app_commands.Command) and hasattr(cmd, 'name') and cmd.name == "mega":
            mega = cmd
            break
        if isinstance(cmd, app_commands.Group) and cmd.name == "mega":
            mega = cmd
            break
    if mega is None:
        # Fallback: create it if not exists
        mega = app_commands.Group(name="mega", description="Mega toolkit")
        bot.tree.add_command(mega)
    await bot.add_cog(Music(bot, mega))
