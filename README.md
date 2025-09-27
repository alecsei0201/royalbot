# RoyalBot — Fly.io build (55+ bundled cogs)
## Локально
```powershell
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. .\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
py -m app.tools.self_test
py -m app.bot
```
## Fly.io
```bash
fly launch --copy-config --name royalbotrl --no-deploy
fly secrets set DISCORD_TOKEN=xxxxx OWNER_ID=4904xxxxx
fly deploy --ha=false --now
fly logs
```
