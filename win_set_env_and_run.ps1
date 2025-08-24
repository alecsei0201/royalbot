
# Быстрый запуск без .env (заполните значения и запустите этот скрипт правой кнопкой → Run with PowerShell)
param(
  [string]$Token = "",
  [string]$OwnerId = ""
)
if (-not $Token -or -not $OwnerId) {
  Write-Host "Укажите параметры: -Token <DISCORD_TOKEN> -OwnerId <OWNER_ID>"
  exit 1
}
$env:DISCORD_TOKEN = $Token
$env:OWNER_ID      = $OwnerId

# Активируем venv, ставим зависимости и запускаем
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
  . .\.venv\Scripts\Activate.ps1
} else {
  py -m venv .venv
  . .\.venv\Scripts\Activate.ps1
}
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m app.tools.self_test
py -m app.bot
