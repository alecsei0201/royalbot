import discord
from discord.ext import commands
from discord import app_commands
class Poll(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="poll", description="Опрос: вопрос;вариант1;вариант2;...")
    async def poll(self, it: discord.Interaction, text: str):
        parts=[p.strip() for p in text.split(";") if p.strip()]
        if len(parts)<3: 
            await it.response.send_message("Нужно: вопрос;вариант1;вариант2;...", ephemeral=True); return
        q, opts = parts[0], parts[1:]
        msg = await it.channel.send("**"+q+"**\n" + "\n".join(f"{i+1}. {o}" for i,o in enumerate(opts)))
        nums = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
        for i,_ in enumerate(opts): await msg.add_reaction(nums[i])
        await it.response.send_message("Создано!", ephemeral=True)
async def setup(bot): await bot.add_cog(Poll(bot))
