import discord
from discord.ext import commands
from discord import app_commands
class Moderation(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="kick", description="Кикнуть пользователя")
    async def kick(self, it: discord.Interaction, member: discord.Member, reason: str=""):
        await member.kick(reason=reason or f"By {it.user}"); await it.response.send_message(f"Кикнут: {member}", ephemeral=True)
    @app_commands.command(name="ban", description="Забанить пользователя")
    async def ban(self, it: discord.Interaction, member: discord.Member, reason: str=""):
        await member.ban(reason=reason or f"By {it.user}"); await it.response.send_message(f"Бан: {member}", ephemeral=True)
    @app_commands.command(name="purge", description="Удалить N сообщений")
    async def purge(self, it: discord.Interaction, amount: int):
        if not it.channel: return
        await it.response.defer(ephemeral=True); deleted=await it.channel.purge(limit=amount)
        await it.followup.send(f"Удалено: {len(deleted)}", ephemeral=True)
async def setup(bot): await bot.add_cog(Moderation(bot))
