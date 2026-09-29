@echo off
cd /d %~dp0
if not exist venv\Scripts\activate.bat (
  echo Virtual environment not found. Run setup_windows.cmd first.
  pause
  exit /b 1
)
if not exist server\.env (
  echo server\.env not found. Run setup_windows.cmd first.
  pause
  exit /b 1
)
start "VeriShield API" cmd /k "cd /d %~dp0 && call venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --app-dir server --port 8000"
start "VeriShield Client" cmd /k "cd /d %~dp0 && npm run dev --prefix client"
echo VeriShield is starting. Open http://localhost:5173
