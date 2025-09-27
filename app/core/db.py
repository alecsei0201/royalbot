import aiosqlite, pathlib
class DB:
    def __init__(self, path: str):
        self.path=path; self.conn=None
    async def connect(self):
        pathlib.Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = await aiosqlite.connect(self.path)
        await self.conn.execute("PRAGMA journal_mode=WAL;")
        await self.conn.execute("PRAGMA synchronous=NORMAL;")
    async def migrate(self):
        assert self.conn
        await self.conn.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT)")
        await self.conn.execute("""CREATE TABLE IF NOT EXISTS warns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER, user_id INTEGER, mod_id INTEGER,
            reason TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        await self.conn.execute("""CREATE TABLE IF NOT EXISTS levels (
            guild_id INTEGER, user_id INTEGER, xp INTEGER DEFAULT 0, level INTEGER DEFAULT 0,
            PRIMARY KEY (guild_id, user_id))""")
        await self.conn.execute("""CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER, user_id INTEGER, message TEXT, due TIMESTAMP)""")
        await self.conn.execute("""CREATE TABLE IF NOT EXISTS notes (
            guild_id INTEGER, user_id INTEGER, note TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        await self.conn.commit()
    async def close(self):
        if self.conn: await self.conn.close(); self.conn=None
