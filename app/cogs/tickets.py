from __future__ import annotations
import logging, discord
from discord.ext import commands
from ..core.db import DB
from ..core.config import get_settings

log = logging.getLogger(__name__)

CATEGORY_NAME = "tickets"

class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot, db: DB):
        self.bot = bot
        self.db = db
        self.enabled = get_settings().enable_tickets

    @commands.hybrid_command(description="Открыть тикет")
    async def ticket(self, ctx: commands.Context, *, topic: str = "Вопрос"):
        if not self.enabled:
            await ctx.reply("Тикеты отключены.")
            return

        guild = ctx.guild
        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
        if category is None:
            category = await guild.create_category(CATEGORY_NAME, reason="Tickets category")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        channel = await guild.create_text_channel(f"ticket-{ctx.author.name}", category=category, overwrites=overwrites)
        await self.db.conn.execute(
            "INSERT INTO tickets (guild_id, user_id, channel_id, status) VALUES (?, ?, ?, ?)",
            (guild.id, ctx.author.id, channel.id, "open")
        )
        await self.db.conn.commit()
        await ctx.reply(f"Создан канал {channel.mention}")

    @commands.hybrid_command(description="Закрыть текущий тикет")
    @commands.has_guild_permissions(manage_channels=True)
    async def close(self, ctx: commands.Context):
        ch = ctx.channel
        if isinstance(ch, discord.TextChannel) and ch.category and ch.category.name == CATEGORY_NAME:
            await ch.edit(name=ch.name.replace("ticket", "closed"))
            await self.db.conn.execute("UPDATE tickets SET status='closed' WHERE channel_id=?", (ch.id,))
            await self.db.conn.commit()
            await ctx.reply("Тикет закрыт.")
        else:
            await ctx.reply("Эта команда доступна только в канале тикета.")

async def setup(bot: commands.Bot):
    db: DB = bot.db  # type: ignore
    await bot.add_cog(Tickets(bot, db))
