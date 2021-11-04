# safety-vision-platform

## Description

SafetyVision REST APIs, video streaming APIs, and safety supervisor alerting.

## Prerequisites
Install `docker-compose` using [these instructions](https://docs.docker.com/compose/install/). If you are using Windows/Mac, the easiest way to do this is to install [Docker Desktop](https://www.docker.com/products/docker-desktop).

Install `make` for your shell of choice.

## Setup

1. Clone this repo and `cd` to this projects root directory.

2. Run setup:
```
make setup
```

3. Run the application:
```
make up
```

4. Visit http://localhost:8000/api/ to verify everything is running.

5. Shut the application down:
```
make down
```

