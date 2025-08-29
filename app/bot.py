import logging, os, py_compile, shutil, asyncio
import discord
from discord.ext import commands
from app.core.config import get_settings
from app.core.db import DB
from app import health as health_server

log = logging.getLogger("royalbot")

class RoyalBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.guilds = True
        intents.message_content = True
        super().__init__(command_prefix=self._prefix, intents=intents)
        self.db: DB | None = None
        self.synced = False

    @staticmethod
    async def _prefix(bot, message):
        try:
            from app.core.config import get_settings
            return get_settings().prefix
        except Exception:
            return "!"

    async def setup_hook(self):
        # DB + core cogs
        s = get_settings()
        self.db = DB(s.db_path)
        await self.db.connect(); await self.db.migrate()

        for ext in [
            "app.cogs.admin",
            "app.cogs.moderation",
            "app.cogs.automod",
            "app.cogs.tickets",
            "app.cogs.leveling",
            "app.cogs.welcome",
            "app.cogs.utilities",
            "app.cogs.diag",
        ]:
            try:
                await self.load_extension(ext)
                log.info("Loaded core: %s", ext)
            except Exception as e:
                log.exception("Failed to load core %s: %s", ext, e)

        await self._load_plugins_from_dir("app/ext/plugins")

        try:
            s = get_settings()
            if s.test_guild_id:
                await self.tree.sync(guild=discord.Object(id=s.test_guild_id))
            else:
                await self.tree.sync()
            self.synced = True
            log.info("Slash commands synced.")
        except Exception:
            log.exception("Slash sync failed")

    async def _load_plugins_from_dir(self, path: str):
        os.makedirs("app/ext/quarantine", exist_ok=True)
        if not os.path.isdir(path): return
        for root, _, files in os.walk(path):
            for f in files:
                if not f.endswith(".py") or f.startswith("_"): continue
                full = os.path.join(root, f)
                mod = full.replace("/", ".").replace("\\", ".")[:-3]
                if "app.ext.plugins" not in mod: continue
                try:
                    py_compile.compile(full, doraise=True)
                except Exception as e:
                    shutil.move(full, os.path.join("app/ext/quarantine", f))
                    log.warning("Quarantined %s: %s", f, e)
                    continue
                try:
                    await self.load_extension(mod)
                    log.info("Loaded plugin: %s", mod)
                except Exception as e:
                    shutil.move(full, os.path.join("app/ext/quarantine", f))
                    log.warning("Plugin failed %s -> quarantine: %s", mod, e)

async def main():
    # 1) health-сервер поднимаем СРАЗУ — до логина в Discord
    asyncio.create_task(health_server.start_health_server())

    # 2) запускаем бота
    s = get_settings()
    logging.basicConfig(
        level=getattr(logging, s.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    bot = RoyalBot()
    try:
        await bot.start(s.token)
    except Exception as e:
        # Если логин/рантайм упали — не гасим процесс, чтобы Fly checks проходили,
        # а ты видел логи и мог починить токен/права.
        log.exception("Bot crashed/failed to start: %s", e)
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())