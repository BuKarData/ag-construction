#!/bin/bash
# Skrypt uruchomienia projektu AG Construction

echo "========================================"
echo "  AG Construction – Setup"
echo "========================================"

# Utwórz i aktywuj środowisko wirtualne
python -m venv venv
source venv/bin/activate  # Linux/Mac
# Dla Windows: venv\Scripts\activate

# Zainstaluj zależności
pip install -r requirements.txt

# Utwórz plik .env (opcjonalnie)
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Skopiowano .env.example do .env – uzupełnij dane produkcyjne"
fi

# Migracje
python manage.py makemigrations oferty
python manage.py migrate

# Utwórz superużytkownika
python manage.py create_superuser

# Zbierz pliki statyczne
python manage.py collectstatic --noinput

echo ""
echo "========================================"
echo "  Uruchom serwer:"
echo "  python manage.py runserver"
echo "  Panel: http://127.0.0.1:8000/admin/"
echo "  Login: admin"
echo "  Hasło: AGConstruction2025!"
echo "========================================"
