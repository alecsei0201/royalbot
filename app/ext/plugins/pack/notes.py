import discord
from discord.ext import commands
from discord import app_commands
class Notes(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="note_add", description="Добавить заметку")
    async def note_add(self, it: discord.Interaction, text: str):
        await self.bot.db.conn.execute("INSERT INTO notes (guild_id,user_id,note) VALUES (?,?,?)", (it.guild_id, it.user.id, text))
        await self.bot.db.conn.commit(); await it.response.send_message("Добавлено.", ephemeral=True)
    @app_commands.command(name="note_list", description="Показать мои заметки")
    async def note_list(self, it: discord.Interaction):
        cur=await self.bot.db.conn.execute("SELECT note,created_at FROM notes WHERE guild_id=? AND user_id=? ORDER BY created_at DESC LIMIT 10",(it.guild_id,it.user.id))
        rows=await cur.fetchall()
        await it.response.send_message("\n".join(f"- {r[0]}" for r in rows) if rows else "Пусто.", ephemeral=True)
async def setup(bot): await bot.add_cog(Notes(bot))
