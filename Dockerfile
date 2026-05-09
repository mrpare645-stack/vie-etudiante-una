FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY=temp-key-for-build
ENV DB_NAME=placeholder

EXPOSE 8000

CMD ["sh", "-c", "mkdir -p /code/staticfiles && python manage.py collectstatic --noinput && python manage.py migrate --noinput --fake-initial || true && python manage.py migrate --noinput --fake && gunicorn una_site.wsgi:application --bind 0.0.0.0:8000 --workers 3"]