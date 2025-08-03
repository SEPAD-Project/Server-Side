@echo off
echo ============================================================
echo ^>^>^> Starting Web Update Process
echo ============================================================

cd /d C:\Users\Administrator\Documents\WebApplication\scripts

echo ^>^>^> Fetching latest code from Git
git fetch --all
git reset --hard origin/main
git clean -fd

echo.
echo ^>^>^> Terminating existing Django and Celery processes...
call stop_server.bat

echo.
echo ^>^>^> Starting new Django and Celery processes
call start_server.bat

echo.
echo ============================================================
echo ^>^>^> Web Update and Restart Completed Successfully
echo ============================================================
