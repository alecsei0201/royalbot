import discord
from discord.ext import commands
from discord import app_commands
TAGS={}
class Tags(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="tag_set", description="Создать/обновить тэг")
    async def tag_set(self, it: discord.Interaction, name: str, value: str):
        guild=it.guild_id; TAGS.setdefault(guild,{})[name]=value; await it.response.send_message("Сохранено.", ephemeral=True)
    @app_commands.command(name="tag", description="Показать тэг")
    async def tag(self, it: discord.Interaction, name: str):
        await it.response.send_message(TAGS.get(it.guild_id,{}).get(name,"нет такого"))
async def setup(bot): await bot.add_cog(Tags(bot))
