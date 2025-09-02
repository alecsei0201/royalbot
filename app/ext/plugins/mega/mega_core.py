import discord
from discord import app_commands, Interaction, Embed, Member, TextChannel, Role
from discord.ext import commands

# Группа: /mega <subcommand>
mega = app_commands.Group(name="mega", description="Mega toolkit: admin & utilities")


def require_perms(**perms):
    def decorator(fn):
        async def wrapper(interaction: Interaction, *args: object, **kwargs: object):
            if not interaction.user.guild_permissions.administrator:
                missing = [
                    k for k, v in perms.items()
                    if v and not getattr(interaction.user.guild_permissions, k, False)
                ]
                if missing:
                    await interaction.response.send_message(
                        f"Недостаточно прав: требуется {', '.join(missing)}", ephemeral=True
                    )
                    return
            return await fn(interaction, *args, **kwargs)
        return wrapper
    return decorator


class Mega(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------- utils ----------
    @mega.command(name="ping", description="Проверить задержку бота")
    async def m_ping(self, interaction: Interaction):
        await interaction.response.send_message(
            f"Pong! {round(self.bot.latency * 1000)}ms", ephemeral=True
        )

    @mega.command(name="avatar", description="Показать аватар пользователя")
    async def m_avatar(self, interaction: Interaction, user: Member | None = None):
        user = user or interaction.user
        embed = Embed(title=f"Аватар {user}", color=discord.Color.blurple())
        embed.set_image(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    # ---------- moderation ----------
    @mega.command(name="lock", description="Закрыть текущий канал для @everyone")
    @require_perms(manage_channels=True)
    async def m_lock(self, interaction: Interaction):
        chan = interaction.channel
        assert isinstance(chan, TextChannel)
        overwrites = chan.overwrites_for(interaction.guild.default_role)
        overwrites.send_messages = False
        await chan.set_permissions(interaction.guild.default_role, overwrite=overwrites)
        await interaction.response.send_message("🔒 Канал заблокирован", ephemeral=True)

    @mega.command(name="unlock", description="Открыть текущий канал для @everyone")
    @require_perms(manage_channels=True)
    async def m_unlock(self, interaction: Interaction):
        chan = interaction.channel
        assert isinstance(chan, TextChannel)
        overwrites = chan.overwrites_for(interaction.guild.default_role)
        overwrites.send_messages = None
        await chan.set_permissions(interaction.guild.default_role, overwrite=overwrites)
        await interaction.response.send_message("🔓 Канал открыт", ephemeral=True)

    @mega.command(name="clean", description="Удалить N сообщений (до 100)")
    @require_perms(manage_messages=True)
    async def m_clean(self, interaction: Interaction, amount: app_commands.Range[int, 1, 100]):
        await interaction.response.defer(ephemeral=True, thinking=True)
        chan = interaction.channel
        assert isinstance(chan, TextChannel)
        deleted = await chan.purge(limit=amount, before=interaction.created_at)
        await interaction.followup.send(f"🧹 Удалено сообщений: {len(deleted)}", ephemeral=True)

    @mega.command(name="slowmode", description="Установить медленный режим")
    @require_perms(manage_channels=True)
    async def m_slowmode(self, interaction: Interaction, delay: app_commands.Range[int, 0, 21600]):
        chan = interaction.channel
        assert isinstance(chan, TextChannel)
        await chan.edit(slowmode_delay=delay)
        await interaction.response.send_message(f"⏱️ Slowmode: {delay}s", ephemeral=True)

    @mega.command(name="nick", description="Сменить ник участнику")
    @require_perms(manage_nicknames=True)
    async def m_nick(self, interaction: Interaction, member: Member, nickname: str | None = None):
        await member.edit(nick=nickname)
        await interaction.response.send_message("✅ Ник изменён.", ephemeral=True)

    # ---------- info ----------
    @mega.command(name="roleinfo", description="Информация о роли")
    async def m_roleinfo(self, interaction: Interaction, role: Role):
        embed = Embed(title=f"Роль: {role.name}", color=role.color or discord.Color.blurple())
        embed.add_field(name="ID", value=str(role.id))
        embed.add_field(name="Участников", value=str(sum(1 for m in interaction.guild.members if role in m.roles)))
        embed.add_field(name="Создана", value=discord.utils.format_dt(role.created_at, style='R'))
        embed.add_field(name="Позиция", value=str(role.position))
        embed.set_footer(text=f"Покрас: {role.color}")
        await interaction.response.send_message(embed=embed)

    @mega.command(name="serverinfo", description="Информация о сервере")
    async def m_serverinfo(self, interaction: Interaction):
        g = interaction.guild
        embed = Embed(title=g.name, color=discord.Color.blurple())
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        embed.add_field(name="ID", value=str(g.id))
        embed.add_field(name="Участников", value=str(g.member_count))
        embed.add_field(name="Создан", value=discord.utils.format_dt(g.created_at, style='R'))
        embed.add_field(name="Каналов", value=str(len(g.channels)))
        await interaction.response.send_message(embed=embed)

    @mega.command(name="userinfo", description="Информация о пользователе")
    async def m_userinfo(self, interaction: Interaction, user: Member | None = None):
        user = user or interaction.user
        roles = [r.mention for r in user.roles if r.name != "@everyone"]
        embed = Embed(title=str(user), color=user.top_role.color if hasattr(user, "top_role") else discord.Color.blurple())
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="ID", value=str(user.id))
        embed.add_field(name="Аккаунт создан", value=discord.utils.format_dt(user.created_at, style='R'))
        if hasattr(user, "joined_at") and user.joined_at:
            embed.add_field(name="Зашёл на сервер", value=discord.utils.format_dt(user.joined_at, style='R'))
        embed.add_field(name="Роли", value=", ".join(roles) if roles else "нет", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    if not any(isinstance(cmd, app_commands.Command) and cmd.name == mega.name for cmd in bot.tree.get_commands()):
        bot.tree.add_command(mega)
    await bot.add_cog(Mega(bot))