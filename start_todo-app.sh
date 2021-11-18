#!/bin/sh
gunicorn --error-logfile /home/Logs/gunicorn_error.log --access-logfile /home/Logs/gunicorn_access.log --bind 0.0.0.0:$PORT "todo_app.app:create_app()"