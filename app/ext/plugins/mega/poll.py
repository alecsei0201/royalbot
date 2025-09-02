from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    class PollView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=300)
            self.votes = {"✅": 0, "❌": 0}
        @discord.ui.button(label="Да", style=discord.ButtonStyle.success, emoji="✅")
        async def yes(self, interaction: Interaction, button: discord.ui.Button):
            self.votes["✅"] += 1
            await interaction.response.defer()
        @discord.ui.button(label="Нет", style=discord.ButtonStyle.danger, emoji="❌")
        async def no(self, interaction: Interaction, button: discord.ui.Button):
            self.votes["❌"] += 1
            await interaction.response.defer()

    @app_commands.command(name="poll2", description="Простое голосование с кнопками.")
    async def poll2(self, interaction: Interaction, вопрос: str):
        embed = Embed(title="Опрос", description=вопрос, color=COLOR)
        view = PollView()
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Poll(bot))
