build:
	docker build -t safety-vision-platform_web-local:latest .

setup:
	docker-compose build

up:
	docker-compose up db -d
	docker-compose up -d

webbash:
	docker-compose exec web /bin/bash

down:
	docker-compose down

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

