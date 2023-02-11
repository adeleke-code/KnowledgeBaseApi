web: gunicorn -b "0.0.0.0:$PORT" -w 3 main_config.wsgi
release: python manage.py migrate