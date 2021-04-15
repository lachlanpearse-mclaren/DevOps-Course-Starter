FROM python:3 as base
WORKDIR /app
COPY ./poetry.toml /app
COPY ./pyproject.toml /app
RUN pip install poetry && poetry install

FROM base as production

RUN apt-get update && \
    apt-get install -y gunicorn 
COPY ./todo_app /app/todo_app
EXPOSE 5000
ENTRYPOINT  $(poetry env info --path)/bin/gunicorn --error-logfile /app/gunicorn_error.log --access-logfile /app/gunicorn_access.log --bind 0.0.0.0:5000 "todo_app.app:create_app()"

FROM base as development

EXPOSE 5000
ENTRYPOINT  poetry run flask run --host 0.0.0.0

FROM base as test
RUN pip install pytest-watch
ENV PATH=$PATH:/app
EXPOSE 4444
ENTRYPOINT  poetry run ptw --poll
