FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=una_site.settings

WORKDIR /code

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn una_site.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
