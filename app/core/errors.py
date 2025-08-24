import logging
from discord.ext import commands

log = logging.getLogger(__name__)

async def setup_error_handlers(bot: commands.Bot):
    @bot.event
    async def on_command_error(ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("У вас нет доступа к этой команде.")
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("Неверные аргументы команды.")
            return
        log.exception("Command error: %s", error)
        await ctx.send("Произошла ошибка при выполнении команды.")
