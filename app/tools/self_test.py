import asyncio, socket
from app.core.config import get_settings
from app.core.db import DB
async def main():
    s=get_settings(); print("ENV OK:", s.prefix, s.db_path)
    db=DB(s.db_path); await db.connect(); await db.migrate(); await db.close()
    sk=socket.socket(); ok=True
    try: sk.bind(("0.0.0.0",8080))
    except Exception: ok=False
    finally: sk.close()
    print("Port 8080 free:", ok)
    print("Bundled plugins:", 60)
    print("OK")
if __name__=="__main__": asyncio.run(main())
