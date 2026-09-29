@echo off
setlocal
cd /d %~dp0

if not exist venv (
  echo [1/4] Creating Python virtual environment...
  python -m venv venv
)

call venv\Scripts\activate.bat

echo [2/4] Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r server\requirements.txt

echo [3/4] Installing frontend dependencies...
call npm install
call npm install --prefix client

if not exist server\.env (
  echo [4/4] Creating server\.env...
  copy server\.env.example server\.env >nul
) else (
  echo [4/4] server\.env already exists - leaving it unchanged.
)

echo.
echo Setup complete.
echo Now open server\.env and set GEMINI_API_KEY and JWT_SECRET.
echo Then run run_windows.cmd
pause
