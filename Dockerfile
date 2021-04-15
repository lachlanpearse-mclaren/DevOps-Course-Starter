FROM python:3 as base

FROM base as production

WORKDIR /app
RUN apt-get update && \
    apt-get install -y gunicorn && \
    pip install poetry
COPY ./todo_app /app/todo_app
COPY ./poetry.toml /app
COPY ./pyproject.toml /app
RUN poetry install
EXPOSE 5000
ENTRYPOINT  $(poetry env info --path)/bin/gunicorn --error-logfile /app/gunicorn_error.log --access-logfile /app/gunicorn_access.log --bind 0.0.0.0:5000 "todo_app.app:create_app()"

FROM base as development

WORKDIR /app
COPY ./poetry.toml /app
COPY ./pyproject.toml /app
RUN pip install poetry && \
    poetry install
EXPOSE 5000
ENTRYPOINT  poetry run flask run --host 0.0.0.0

