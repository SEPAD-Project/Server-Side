@echo off
cd C:/Users/Administrator/Documents/web
git fetch --all
git reset --hard origin/main
git clean -fd
taskkill /IM waitress-serve.exe /F
start "" /B waitress-serve --port=2568 source.wsgi:app