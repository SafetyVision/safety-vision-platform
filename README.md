# safety-vision-platform

## Description

SafetyVision REST APIs, video streaming APIs, and safety supervisor alerting.

## Prerequisites
Install `docker-compose` using [these instructions](https://docs.docker.com/compose/install/). If you are using Windows/Mac, the easiest way to do this is to install [Docker Desktop](https://www.docker.com/products/docker-desktop).

Install `make` for your shell of choice.

## Setup

1. Clone this repo and `cd` to this projects root directory.

2. Build and run the docker images:
```
make build
make up
```

3. Run the database migrations (if you have issues running this just try again in a few seconds):
```
make migrate
```

4. Visit http://localhost:8000/api/ to verify everything is running.

5. Shut the application down:
```
make down
```

