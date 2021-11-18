#!/bin/sh
gunicorn --error-logfile /home/LogFiles/gunicorn_error.log --access-logfile /home/LogFiles/gunicorn_access.log --bind 0.0.0.0:$PORT "todo_app.app:create_app()"