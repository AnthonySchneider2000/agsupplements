@echo off

start cmd /k "cd frontend && ng serve"
start cmd /k "python manage.py runserver"
