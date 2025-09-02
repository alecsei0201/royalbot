import discord, datetime, asyncio
from discord.ext import commands
from discord import app_commands
class Remind(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="remind", description="Напомнить через N минут")
    async def remind(self, it: discord.Interaction, minutes: int, text: str):
        due = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
        await self.bot.db.conn.execute("INSERT INTO reminders (guild_id,user_id,message,due) VALUES (?,?,?,?)", (it.guild_id,it.user.id,text,due.isoformat()))
        await self.bot.db.conn.commit(); await it.response.send_message(f"Ок, напомню в {minutes} мин.", ephemeral=True)
async def setup(bot): await bot.add_cog(Remind(bot))
