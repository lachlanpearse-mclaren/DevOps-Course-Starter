#!/bin/sh
gunicorn --bind 0.0.0.0:$PORT "todo_app.app:create_app()"