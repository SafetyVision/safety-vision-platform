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


build:
	docker-compose build

setup: build up makemigrations migrate down