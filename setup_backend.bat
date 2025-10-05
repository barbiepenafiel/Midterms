@echo off
echo ========================================
echo   Oursfolio Django Backend Setup
echo ========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate.bat

echo [1/5] Making migrations...
python manage.py makemigrations
echo.

echo [2/5] Applying migrations...
python manage.py migrate
echo.

echo [3/5] Creating superuser (optional)...
echo Skip this if you already have a superuser
python manage.py createsuperuser
echo.

echo [4/5] Collecting static files...
python manage.py collectstatic --noinput
echo.

echo [5/5] Setup complete!
echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo 1. Start Django server:    python manage.py runserver
echo 2. Start Celery worker:    celery -A backend worker --loglevel=info --pool=solo
echo 3. Start Celery beat:      celery -A backend beat --loglevel=info
echo 4. Access Swagger docs:    http://localhost:8000/swagger/
echo 5. Access Admin panel:     http://localhost:8000/admin/
echo ========================================
echo.
pause
