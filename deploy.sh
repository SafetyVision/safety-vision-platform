#!/bin/sh

ssh -o StrictHostKeyChecking=no ubuntu@34.205.100.22 << 'ENDSSH'
  docker login --username safetyvision --password $DOCKER_PASSWORD
  docker pull safetyvision/safety-vision-platform
  docker-compose -f docker-compose.prod.yml up -d web
ENDSSH
