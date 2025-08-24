"""
Fetch 150+ open-source Discord cogs from GitHub into app/ext/plugins.
- Filters by permissive licenses.
- Avoids duplicate filenames.
- Optionally uses GITHUB_TOKEN for higher rate limits.
Usage:
  python tools/fetch_cogs.py --limit 250 --min-stars 10 --topics moderation,utility,music,games,automod,admin
"""
import os, sys, argparse, asyncio, aiohttp, re, base64, pathlib, json, shutil
from typing import List, Dict, Any, Optional

ALLOW_LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "MPL-2.0", "Unlicense", "ISC"}

SEARCH_QUERIES = [
    'discord.py cogs language:Python stars:>=10',
    'discord bot cogs language:Python stars:>=10',
    'discord.ext commands Cog language:Python stars:>=10',
    'topic:discord-bot language:Python stars:>=10',
]

def repo_ok(item: Dict[str, Any]) -> bool:
    name = item.get("full_name","").lower()
    return True

def sanitize_filename(path: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", path)

async def fetch_json(session: aiohttp.ClientSession, url: str) -> Any:
    async with session.get(url) as r:
        r.raise_for_status()
        return await r.json()

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=250)
    ap.add_argument("--min-stars", type=int, default=10)
    ap.add_argument("--topics", type=str, default="moderation,utility,automod,games,levels,welcome,logging,tickets,roles,starboard,webhook,reminders,fun,images,ai,tts,music")
    ap.add_argument("--out", type=str, default="app/ext/plugins")
    args = ap.parse_args()

    gh = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if gh:
        headers["Authorization"] = f"Bearer {gh}"

    outdir = pathlib.Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    # Collect repos
    repos = {}
    async with aiohttp.ClientSession(headers=headers) as session:
        page = 1
        while len(repos) < args.limit and page <= 10:
            for q in SEARCH_QUERIES:
                url = f"https://api.github.com/search/repositories?q={q}&per_page=50&page={page}&sort=stars&order=desc"
                try:
                    data = await fetch_json(session, url)
                except Exception:
                    continue
                for item in data.get("items", []):
                    if item.get("stargazers_count",0) < args.min_stars:
                        continue
                    repos[item["full_name"]] = item
            page += 1

        print(f"Found candidate repos: {len(repos)}")

        # Filter by license
        selected = []
        for full in list(repos.keys()):
            try:
                lic = await fetch_json(session, f"https://api.github.com/repos/{full}/license")
                spdx = (lic.get("license") or {}).get("spdx_id")
                if spdx in ALLOW_LICENSES:
                    selected.append(full)
            except Exception:
                # if no license API, skip to be safe
                continue

        print(f"Repos with permissive licenses: {len(selected)}")

        # For each repo: fetch files: try 'cogs', 'extensions', or any *cog*.py
        downloaded = 0
        for full in selected:
            if downloaded >= args.limit:
                break
            try:
                contents = await fetch_json(session, f"https://api.github.com/repos/{full}/contents")
            except Exception:
                continue

            # queue of paths to explore
            queue = []
            for entry in contents:
                if entry["type"] == "dir" and entry["name"].lower() in {"cogs","extensions","plugins"}:
                    queue.append(entry["path"])
                if entry["type"] == "file" and entry["name"].endswith(".py") and ("cog" in entry["name"].lower() or "ext" in entry["name"].lower()):
                    queue.append(entry["path"])

            seen_paths = set()
            while queue and downloaded < args.limit:
                p = queue.pop(0)
                if p in seen_paths:
                    continue
                seen_paths.add(p)
                try:
                    listing = await fetch_json(session, f"https://api.github.com/repos/{full}/contents/{p}")
                except Exception:
                    continue
                if isinstance(listing, dict) and listing.get("type") == "file":
                    listing = [listing]
                for node in listing:
                    if node["type"] == "dir":
                        queue.append(node["path"])
                    elif node["type"] == "file" and node["name"].endswith(".py"):
                        # download file content
                        try:
                            meta = await fetch_json(session, node["url"])
                            encoded = meta.get("content")
                            if meta.get("encoding") == "base64" and encoded:
                                raw = base64.b64decode(encoded)
                                fname = sanitize_filename(f"{full.replace('/','__')}__{node['path'].replace('/','__')}")
                                dest = outdir / fname
                                if not dest.exists():
                                    dest.write_bytes(raw)
                                    downloaded += 1
                                    print(f"+ {dest.name}")
                        except Exception:
                            continue

        print(f"Downloaded Python modules: {downloaded}")

if __name__ == "__main__":
    asyncio.run(main())
