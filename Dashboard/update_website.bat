@echo off
cd C:/Users/Administrator/Documents/web
git fetch --all
git reset --hard origin/main
git clean -fd
taskkill /IM waitress-serve.exe /F
taskkill /IM celery.exe /F
start "Celery Worker" cmd /k "cd C:/Users/Administrator/Documents/web && .venv\Scripts\activate && celery -A source.celery worker --loglevel=info -P threads"
waitress-serve --listen=0.0.0.0:2568 source.app:app
