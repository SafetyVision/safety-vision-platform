# safety-vision-platform

SafetyVision REST APIs, video streaming APIs, and safety supervisor alerting.

## Build
Build the Docker image:
```
make build
```

## Run the app
Setup:
```
make build
```

Set the `AWS_ACCESS_KEY_ID` and `AWS_SECRECT_ACCESS_KEY` environment variables.

Run:
```
make up
```

Run migrations:
```
make migrate
```

Shutdown:
```
make down
```

To run tests in development you can either start the application manually with `make up` and then run `make webbash` to be able to run tests with `python manage.py test`. Alternatively, without the application running, simply run:
```
make test
```
