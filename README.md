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
