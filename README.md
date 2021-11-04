# safety-vision-platform

## Description

SafetyVision REST APIs, video streaming APIs, and safety supervisor alerting.

## Prerequisites
Run `python -V` and make sure you are running Python3.

## Setup

Clone this repo.

Follow the [MDN steps](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment) to setup a Django development environment for your OS.

1. For Windows, install `virutalenv`:

```
pip3 install virtualenvwrapper-win
```

2. Create your virtual environment:

```
mkvirtualenv safety-vision-platform -a path\to\safety-vision-platform
```

3. Activate your virtual environment:

```
~\Envs\safety-vision-platform\Scripts\activate.ps1
```

4. Install Django:

```
pip3 install django~=3.1
```

Check that your installation was successful with this command that should produce a 3.x.x version number:
```
python -m django --version
```

5. Install Django REST framework:
```
pip3 install djangorestframework
```

6. Run migrations:

```
python manage.py migrate
```

7. Run the server and visit http://127.0.0.1:8000/api to test that the application is running.
```
python manage.py runserver
```

You should be up and running!
