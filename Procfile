web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 2
worker: celery -A config worker -l info --concurrency=2
beat: celery -A config beat -l info
