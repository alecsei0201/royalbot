import discord
from discord.ext import commands
BAD={"badword1","badword2","плохое"}
class AutoMod(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if not m.guild or m.author.bot: return
        t=m.content.lower()
        if any(b in t for b in BAD):
            try: await m.delete()
            except: pass
            await m.channel.send(f"{m.author.mention}, соблюдайте правила.", delete_after=5)
async def setup(bot): await bot.add_cog(AutoMod(bot))
