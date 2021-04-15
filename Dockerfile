FROM python:3
WORKDIR /app
RUN apt-get update && \
    apt-get install -y gunicorn && \
    pip install poetry

COPY ./todo_app /app/todo_app
COPY ./.env /app
COPY ./poetry.toml /app
COPY ./pyproject.toml /app
COPY ./README.md /app

RUN cd /app && poetry install
EXPOSE 5000
ENTRYPOINT $(poetry env info --path)/bin/gunicorn --error-logfile /app/gunicorn_error.log --access-logfile /app/gunicorn_access.log --bind 0.0.0.0:5000 "todo_app.app:create_app()"
