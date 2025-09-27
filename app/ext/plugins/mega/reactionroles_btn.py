from __future__ import annotations
import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import asyncio
COLOR = 0x2b2d31


class ReactionRolesBtn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


class RoleButton(discord.ui.Button):
    def __init__(self, role_id: int, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.role_id = role_id
    async def callback(self, interaction: Interaction):
        role = interaction.guild.get_role(self.role_id) if interaction.guild else None
        if not role:
            return await interaction.response.send_message("Роль не найдена.", ephemeral=True)
        if role in interaction.user.roles:  # type: ignore
            await interaction.user.remove_roles(role)  # type: ignore
            await interaction.response.send_message(f"❌ Снял роль {role.mention}", ephemeral=True)
        else:
            await interaction.user.add_roles(role)  # type: ignore
            await interaction.response.send_message(f"✅ Выдал роль {role.mention}", ephemeral=True)

class RRView(discord.ui.View):
    def __init__(self, roles: list[tuple[int,str]]):
        super().__init__(timeout=None)
        for rid, name in roles:
            self.add_item(RoleButton(rid, name))

    @app_commands.command(name="rr_panel", description="Панель ролей (кнопки).")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def rr_panel(self, interaction: Interaction, role1: discord.Role, role2: discord.Role | None = None, role3: discord.Role | None = None):
        roles = [(role1.id, role1.name)]
        if role2: roles.append((role2.id, role2.name))
        if role3: roles.append((role3.id, role3.name))
        embed = Embed(title="Роли по кнопкам", description="Нажмите, чтобы выдать/снять роль.", color=COLOR)
        await interaction.response.send_message(embed=embed, view=RRView(roles))


async def setup(bot: commands.Bot):
    await bot.add_cog(ReactionRolesBtn(bot))
