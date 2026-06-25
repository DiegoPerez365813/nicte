@echo off
echo Iniciando Nicte (backend + frontend)...

start "Nicte Backend" /D "%~dp0backend" "%~dp0backend\venv_win\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000

set PATH=%PATH%;C:\Program Files\nodejs
start "Nicte Frontend" /D "%~dp0frontend" cmd /k "npm run dev"

echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Se abrieron dos ventanas (Nicte Backend y Nicte Frontend). No las cierres mientras uses la app.
echo El backend puede tardar unos segundos en estar listo la primera vez.
pause
