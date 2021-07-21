#!/bin/sh
$(poetry env info --path)/bin/gunicorn --error-logfile /app/gunicorn_error.log --access-logfile /app/gunicorn_access.log --bind 0.0.0.0:$PORT "todo_app.app:create_app()"