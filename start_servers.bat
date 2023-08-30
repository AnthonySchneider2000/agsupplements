#!/bin/bash

gnome-terminal -- bash -c "cd frontend && npm run serve"
gnome-terminal -- bash -c "cd backend && python manage.py runserver"
