"""
Run comprehensive offline checks:
- Env validation
- DB read/write
- Plugin compile audit (without execution)
- Health endpoint bind test
Usage:
  python -m app.tools.self_test
"""
from __future__ import annotations
import asyncio, os, py_compile, pathlib, socket
from ..core.config import get_settings
from ..core.db import DB

def check_env():
    s = get_settings()
    assert s.token, "DISCORD_TOKEN is missing"
    return {
        "owner_id": s.owner_id,
        "db_path": s.db_path,
        "features": {
            "automod": s.enable_automod,
            "leveling": s.enable_leveling,
            "tickets": s.enable_tickets,
            "welcome": s.enable_welcome,
            "music": s.enable_music,
        }
    }

async def check_db():
    s = get_settings()
    db = DB(s.db_path)
    await db.connect()
    await db.migrate()
    await db.conn.execute("INSERT OR REPLACE INTO kv (key, value) VALUES ('self_test','ok')")
    await db.conn.commit()
    # read back
    async with db.conn.execute("SELECT value FROM kv WHERE key='self_test'") as cur:
        row = await cur.fetchone()
        assert row and row[0] == 'ok', "DB readback failed"
    await db.close()
    return True

def audit_plugins():
    p = pathlib.Path("app/ext/plugins")
    p.mkdir(parents=True, exist_ok=True)
    ok = 0; bad = 0
    for f in p.glob("*.py"):
        try:
            py_compile.compile(str(f), doraise=True)
            ok += 1
        except Exception:
            bad += 1
    return {"ok": ok, "bad": bad, "total": ok+bad}

def check_port_bind():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", 8080))
        return True
    except Exception as e:
        return False
    finally:
        s.close()

async def main():
    env = check_env()
    db_ok = await check_db()
    audit = audit_plugins()
    port = check_port_bind()
    print("ENV:", env)
    print("DB:", db_ok)
    print("Plugins:", audit)
    print("Port 8080 free:", port)

if __name__ == "__main__":
    asyncio.run(main())
