release: python manage.py migrate
web: daphne pms.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker channels