@echo off
setlocal
cd /d %~dp0

echo VeriShield clean restart
echo ------------------------
echo Closing any existing development servers on ports 8000 and 5173...

for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do taskkill /PID %%P /F >nul 2>nul
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":5173" ^| findstr "LISTENING"') do taskkill /PID %%P /F >nul 2>nul

timeout /t 1 /nobreak >nul
call run_windows.cmd
