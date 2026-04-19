web: python manage.py migrate --run-syncdb && python manage.py collectstatic --noinput && python manage.py create_superuser && gunicorn ag_construction.wsgi --log-file -
