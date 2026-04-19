@echo off
echo ========================================
echo   AG Construction – Setup (Windows)
echo ========================================

python -m venv venv
call venv\Scripts\activate

pip install -r requirements.txt

if not exist .env (
    copy .env.example .env
    echo Skopiowano .env.example do .env
)

python manage.py makemigrations oferty
python manage.py migrate
python manage.py create_superuser
python manage.py collectstatic --noinput

echo.
echo ========================================
echo   Uruchom: python manage.py runserver
echo   Panel:   http://127.0.0.1:8000/admin/
echo   Login:   admin
echo   Haslo:   AGConstruction2025!
echo ========================================
pause
