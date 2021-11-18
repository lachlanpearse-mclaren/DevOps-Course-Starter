#!/bin/sh
gunicorn --error-logfile /var/log/gunicorn_error.log --access-logfile /var/log/gunicorn_access.log --bind 0.0.0.0:$PORT "todo_app.app:create_app()"