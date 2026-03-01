FROM python:3.14-slim
WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE false
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src

RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libpq-dev
RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY src src

RUN DJANGO_SETTINGS_MODULE=scheduling.settings.static python src/manage.py collectstatic --noinput

CMD ["gunicorn", "scheduling.wsgi:application", "--bind", "0.0.0.0:80"]
