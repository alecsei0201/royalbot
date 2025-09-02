import discord, random
from discord.ext import commands
from discord import app_commands
class Choose(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="choose", description="Выбрать из вариантов через ,")
    async def choose(self, it: discord.Interaction, options: str):
        items=[x.strip() for x in options.split(",") if x.strip()]
        await it.response.send_message(random.choice(items) if items else "Нет вариантов")
async def setup(bot): await bot.add_cog(Choose(bot))
