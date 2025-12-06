@echo off
REM Gunicorn startup script for Windows

setlocal enabledelayedexpansion

REM Load environment variables from .env if it exists
if exist .env (
    for /f "delims== tokens=1,2" %%A in (.env) do (
        set "%%A=%%B"
    )
)

REM Set defaults if not defined
if not defined GUNICORN_BIND set "GUNICORN_BIND=0.0.0.0:8000"
if not defined GUNICORN_WORKERS set "GUNICORN_WORKERS=4"
if not defined GUNICORN_WORKER_CLASS set "GUNICORN_WORKER_CLASS=sync"
if not defined GUNICORN_LOG_LEVEL set "GUNICORN_LOG_LEVEL=info"

echo Starting LR3WEB with Gunicorn...
echo Bind: !GUNICORN_BIND!
echo Workers: !GUNICORN_WORKERS!
echo Worker Class: !GUNICORN_WORKER_CLASS!
echo Log Level: !GUNICORN_LOG_LEVEL!
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
)

REM Install/upgrade packages
echo Ensuring dependencies are installed...
pip install -q -r requirements.txt

REM Run Gunicorn
echo.
echo Starting Gunicorn server...
gunicorn ^
    --bind=!GUNICORN_BIND! ^
    --workers=!GUNICORN_WORKERS! ^
    --worker-class=!GUNICORN_WORKER_CLASS! ^
    --log-level=!GUNICORN_LOG_LEVEL! ^
    --config=gunicorn_config.py ^
    LR3_WEB:app

echo.
echo Gunicorn server stopped.
