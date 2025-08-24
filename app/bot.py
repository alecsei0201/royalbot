from __future__ import annotations
import asyncio, logging, os, signal
import discord
from discord.ext import commands
from aiohttp import web
import sentry_sdk

from .core.logging import setup_logging
from .core.config import get_settings
from .core.db import DB
from .core.errors import setup_error_handlers
from .core.health import self_check

setup_logging()
log = logging.getLogger("royalbot")

class RoyalBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True  # нужен для некоторых функций
        s = get_settings()
        super().__init__(
            command_prefix=commands.when_mentioned_or(s.prefix),
            intents=intents,
            help_command=None,
        )
        self.settings = s
        self.db = DB(s.db_path)
        self.http_app: web.Application | None = None
        self.http_runner: web.AppRunner | None = None

    async def setup_hook(self) -> None:
        # Connect DB & migrate
        await self.db.connect()
        await self.db.migrate()

        # Load core cogs
        core_cogs = [
            "app.cogs.admin",
            "app.cogs.utility",
            "app.cogs.moderation",
            "app.cogs.automod",
            "app.cogs.tickets",
            "app.cogs.leveling",
            "app.cogs.welcome",
            "app.cogs.voice_join",
            "app.cogs.music",
        ]
        for ext in core_cogs:
            try:
                await self.load_extension(ext)
            except Exception as e:
                log.exception("Failed to load %s: %s", ext, e)

        # Load external plugins
        await self._load_plugins_from_dir("app/ext/plugins")

        # Error handlers
        await setup_error_handlers(self)

        # Sync slash commands
        if self.settings.test_guild_id:
            try:
                guild = discord.Object(id=self.settings.test_guild_id)
                await self.tree.sync(guild=guild)
                log.info("Synced to test guild %s", self.settings.test_guild_id)
            except Exception:
                log.exception("Guild sync failed")

        # Start HTTP health server
        await self._start_http_server()


    async def _load_plugins_from_dir(self, path: str) -> None:
        import importlib.util, types, pathlib, shutil, py_compile
        if not os.path.isdir(path):
            return

        quarantine_dir = os.path.join(os.path.dirname(path), "quarantine")
        os.makedirs(quarantine_dir, exist_ok=True)

        # Snapshot existing command names (to avoid duplicates)
        existing_names = set(cmd.qualified_name for cmd in list(self.commands))
        existing_names.update(ac.name for ac in list(self.tree.get_commands()))

        for root, _, files in os.walk(path):
            for file in files:
                if not file.endswith(".py") or file.startswith("_"):
                    continue
                full_path = os.path.join(root, file)

                # Fast syntax check without executing third-party code
                try:
                    py_compile.compile(full_path, doraise=True)
                except Exception as e:
                    log.warning("Syntax error in plugin %s: %s. Moving to quarantine.", full_path, e)
                    shutil.move(full_path, os.path.join(quarantine_dir, os.path.basename(full_path)))
                    continue

                # Derive module path under 'app.' namespace
                rel = os.path.relpath(full_path, start=os.path.dirname(os.path.dirname(path))).replace(os.sep, ".")
                if not rel.startswith("app."):
                    rel = f"app.{rel}"
                mod = rel[:-3]  # strip .py

                try:
                    await self.load_extension(mod)
                    # Deduplicate: if plugin introduced commands that already exist, remove new ones
                    dup_removed = 0
                    for cmd in list(self.commands):
                        if cmd.qualified_name in existing_names:
                            self.remove_command(cmd.qualified_name)
                            dup_removed += 1
                    for appcmd in list(self.tree.get_commands()):
                        if appcmd.name in existing_names:
                            self.tree.remove_command(appcmd.name, type=appcmd.type)
                            dup_removed += 1
                    if dup_removed:
                        log.info("Loaded %s with %d duplicate commands pruned.", mod, dup_removed)
                    else:
                        log.info("Loaded %s", mod)
                except Exception as e:
                    log.warning("Failed to load plugin %s: %s. Moving to quarantine.", mod, e)
                    # Move raw file to quarantine for inspection
                    try:
                        shutil.move(full_path, os.path.join(quarantine_dir, os.path.basename(full_path)))
                    except Exception:
                        pass

    async def on_ready(self):
        log.info("Logged in as %s (%s)", self.user, self.user.id)

    async def close(self) -> None:
        await super().close()
        if self.http_runner:
            await self.http_runner.cleanup()
        await self.db.close()

    async def _start_http_server(self) -> None:
        app = web.Application()
        async def healthz(request: web.Request):
            return web.json_response(self_check())
        app.add_routes([web.get("/healthz", healthz)])
        self.http_app = app
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()
        self.http_runner = runner
        log.info("Health server started on :8080")

def run():
    s = get_settings()
    if s.sentry_dsn:
        sentry_sdk.init(s.sentry_dsn, traces_sample_rate=0.1)
    bot = RoyalBot()

    loop = asyncio.get_event_loop()

    def handle_sig(*_):
        log.info("Shutting down...")
        loop.create_task(bot.close())

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, handle_sig)
        except NotImplementedError:
            pass

    bot.run(s.token)

if __name__ == "__main__":
    run()
