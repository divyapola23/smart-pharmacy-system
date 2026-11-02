@echo off
title Smart Pharmacy System - Public Server
cd /d "%~dp0"

echo ========================================================
echo   Smart Pharmacy System - Standalone Public Server
echo ========================================================
echo.
echo Launching server and Cloudflare tunnel outside Antigravity...
echo.

if exist ".\.venv\Scripts\python.exe" (
    ".\.venv\Scripts\python.exe" start_public.py
) else (
    python start_public.py
)

if errorlevel 1 (
    echo.
    echo [ERROR] Encountered an issue starting the application.
    pause
)
