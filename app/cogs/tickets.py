import discord
from discord.ext import commands
from discord import app_commands
class Tickets(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @app_commands.command(name="ticket", description="Создать тикет-канал")
    async def ticket(self, it: discord.Interaction):
        g=it.guild
        ow={g.default_role: discord.PermissionOverwrite(read_messages=False), it.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)}
        ch=await g.create_text_channel(f"ticket-{it.user.name}", overwrites=ow, reason="Ticket")
        await it.response.send_message(f"Создан канал {ch.mention}", ephemeral=True)
async def setup(bot): await bot.add_cog(Tickets(bot))
