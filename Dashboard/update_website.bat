@echo off
cd C:/Users/Administrator/Documents/web
git fetch --all
git reset --hard origin/main
git clean -fd
taskkill /IM waitress-serve.exe /F
waitress-serve --listen=0.0.0.0:2568 source.app:app