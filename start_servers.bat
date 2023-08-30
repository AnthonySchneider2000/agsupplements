@echo off

start cmd /k "cd frontend && npm run serve"
start cmd /k "python manage.py runserver"
