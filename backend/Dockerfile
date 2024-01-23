FROM python:3.10-slim

WORKDIR /backend

COPY . /backend/
RUN pip install -r requirements.txt

CMD python manage.py migrate \
    && python manage.py collectstatic --no-input \
    && gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --log-level info