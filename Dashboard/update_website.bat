@echo off
echo ============================================================
echo ^>^>^> Starting Web Update Process
echo ============================================================

cd /d C:\Users\Administrator\Documents\web

echo ^>^>^> Fetching latest code from Git
git fetch --all
git reset --hard origin/main
git clean -fd

echo.
echo ^>^>^> Terminating existing Celery and Flask processes...

taskkill /IM waitress-serve.exe /F >nul 2>&1
wmic process where "CommandLine like '%%celery%%' and name='python.exe'" call terminate >nul 2>&1
wmic process where "CommandLine like '%%celery%%' and name='cmd.exe'" call terminate >nul 2>&1
wmic process where "CommandLine like '%%waitress%%' and name='python.exe'" call terminate >nul 2>&1
wmic process where "CommandLine like '%%waitress%%' and name='cmd.exe'" call terminate >nul 2>&1
taskkill /FI "WINDOWTITLE eq Celery Worker" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Flask Server" /F >nul 2>&1

echo.
echo ^>^>^> Launching new Celery Worker
start "Celery Worker" cmd /k "cd /d C:\Users\Administrator\Documents\web && .venv\Scripts\activate && python -m celery -A source.celery worker --loglevel=info -P threads"

echo.
echo ^>^>^> Launching Flask Server with Waitress
start "Flask Server" cmd /k "cd /d C:\Users\Administrator\Documents\web && .venv\Scripts\activate && waitress-serve --listen=0.0.0.0:2568 source.app:app"

echo.
echo ============================================================
echo ^>^>^> Web Update and Restart Completed Successfully
echo ============================================================
