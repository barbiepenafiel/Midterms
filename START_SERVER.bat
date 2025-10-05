@echo off
echo.
echo ===============================================
echo   Starting Local Server for Oursfolio
echo ===============================================
echo.
echo Server will run at: http://localhost:8000
echo.
echo Open this URL in your browser:
echo http://localhost:8000/frontend/landing.html
echo.
echo Press Ctrl+C to stop the server
echo ===============================================
echo.

cd /d "%~dp0"
python -m http.server 8000

pause
