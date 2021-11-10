#!/bin/sh

ssh -o StrictHostKeyChecking=no ubuntu@34.205.100.22 << 'ENDSSH'
  export $(cat .env | xargs)
  cd /home/ubuntu/safety-vision-infra
  docker login --username safetyvision --password $DOCKER_PASSWORD
  docker pull safetyvision/safety-vision-platform
  docker-compose up --no-deps -d web
  docker-compose exec web python manage.py collectstatic --no-input
ENDSSH
