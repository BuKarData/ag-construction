release: python manage.py migrate --run-syncdb && python manage.py collectstatic --noinput
web: gunicorn ag_construction.wsgi --log-file -
