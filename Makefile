build:
	docker build -t safety-vision-platform_web-local:latest .

up:
	docker-compose up -d db
	docker-compose up -d

webbash:
	docker-compose exec web /bin/bash

down:
	docker-compose down

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

test: up
	docker-compose exec web python manage.py test
	docker-compose down
