from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class TicketsSimple(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Создать тикет", style=discord.ButtonStyle.primary, custom_id="mega_ticket:create")
    async def create(self, interaction: Interaction, button: discord.ui.Button):
        g = interaction.guild
        if not isinstance(g, discord.Guild):
            return await interaction.response.send_message("Только на сервере.", ephemeral=True)
        overwrites = {
            g.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }
        cat = discord.utils.get(g.categories, name="Tickets") or await g.create_category("Tickets")
        ch = await g.create_text_channel(name=f"ticket-{interaction.user.name}".lower()[:20], category=cat, overwrites=overwrites)
        await interaction.response.send_message(f"Создан канал {ch.mention}", ephemeral=True)

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Закрыть", style=discord.ButtonStyle.danger)
    async def close(self, interaction: Interaction, button: discord.ui.Button):
        ch = interaction.channel
        if isinstance(ch, discord.TextChannel):
            await interaction.response.defer(ephemeral=True)
            await asyncio.sleep(1)
            await ch.delete()

    @app_commands.command(name="ticket_panel", description="Панель тикетов (кнопка открытия).")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def ticket_panel(self, interaction: Interaction):
        embed = Embed(title="Поддержка", description="Нажмите, чтобы создать тикет.", color=COLOR)
        await interaction.response.send_message(embed=embed, view=TicketView())


async def setup(bot: commands.Bot):
    await bot.add_cog(TicketsSimple(bot))
