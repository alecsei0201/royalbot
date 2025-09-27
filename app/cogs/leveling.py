import random, discord
from discord.ext import commands
from discord import app_commands
class Leveling(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if not m.guild or m.author.bot: return
        add=random.randint(1,5)
        await self.bot.db.conn.execute("INSERT INTO levels (guild_id,user_id,xp,level) VALUES (?,?,?,0) ON CONFLICT(guild_id,user_id) DO UPDATE SET xp=xp+excluded.xp", (m.guild.id, m.author.id, add))
        await self.bot.db.conn.commit()
    @app_commands.command(name="rank", description="Показать ваш XP")
    async def rank(self, it: discord.Interaction, member: discord.Member|None=None):
        member=member or it.user
        cur=await self.bot.db.conn.execute("SELECT xp,level FROM levels WHERE guild_id=? AND user_id=?", (it.guild_id, member.id))
        row=await cur.fetchone(); xp=row[0] if row else 0
        await it.response.send_message(f"{member.mention}: XP={xp}")
async def setup(bot): await bot.add_cog(Leveling(bot))
