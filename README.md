# safety-vision-platform

## Description

SafetyVision REST APIs, video streaming APIs, and safety supervisor alerting.

## Prerequisites
Install `docker-compose` using [these instructions](https://docs.docker.com/compose/install/). If you are using Windows/Mac, the easiest way to do this is to install [Docker Desktop](https://www.docker.com/products/docker-desktop).

## Setup

1. Clone this repo and `cd` to this projects root directory.

2. Build the docker images:
```
docker-compose build
```

3. Start the MySql container:
```
docker-compose up db -d
```

4. Start the Django app:
```
docker-compose up web -d
```

5. Start a shell in the `web` container to check that the container is running successfully:
```
docker-compose exec web /bin/bash
```

6. Run any initial database migrations and exit the container's shell:
```
python manage.py migrate
exit
```

7. Go to http://localhost:8000/api/ in your browser and you should be go to go!

8. To shutdown the two running containers:
```
docker-compose down
```

