# WEATHER FORECAST Api

## Dependencies

Tested on Linux and macOS

- Python >= 3.8
- Django 2.2
- Redis
- Postgres

Ubuntu packages for mysql: `postgresql`, `postgresql-contrib`, `libssl-dev`
Ubuntu packages for redis: `redis-server`

## Initial Steps

- Clone repo
- Create (virtualenv env --python=python3) and activate (source env/bin/activate) virtual env
- Install requeriment (pip): pip install -r requirements.txt
- Create database (weather_forecast)

Set any local settings you want in local_settings.py. Don't override settings.py

## Local Settings (DEVELOPMENT)

```
(env) $ cp weather_forecast/local_settings.example.py weather_forecast/local_settings.py
(env) $ cp weather_forecast/secrets.example.py weather_forecast/secrets.py
```

The most important configurations are:

- DATABASES: Database configuration
- SITE_URL
- All configs and keys of external services

## Environment Variables

Create weather_forecast/.env variables or set the environment variables. Use like example weather_forecast/.env.example
https://django-environ.readthedocs.io/en/latest/

## Migrations

`(env) $ python manage.py makemigrations
`(env) $ python manage.py migrate --database=default`

## Static Files

In production. When DEBUG=False it is necessary compile the static files. This is because django dont manage this, you
need to pass to nginx for example. Set in settings:
STATIC_ROOT = "/var/www/example.com/static/" -< When compile store there

Run the command:
`(env) $ python manage.py collectstatic`
Notes: https://docs.djangoproject.com/en/2.2/howto/static-files/deployment/#serving-static-files-from-a-dedicated-server

## Django Extensions

The lib 'django-extensions' provide utils functions. For example we can see the all urls and your reverse names. Add in
installed_apps -> 'django_extensions'

```
(env) $ pip install django-extensions
(env) $ python manage.py show_urls
```

## Run Django App

(env) $ python manage.py runserver 0.0.0.0:port

## Run tests without coverage

`(env) $ python manage.py test`
`(env) $ python manage.py test --keepdb (Use the same database created previously for other tests)`

## Run tests with coverage

`(env) $ coverage run --omit=env/* manage.py test`
`(env) $ coverage html`

Open file htmlcov/index.html to see detail of coverage.

# Documentation

## Swagger

Swagger are available in /swagger only for Debug=True. For access to definition of swagger you need to get the
url: http://localhost:8001/swagger.json with credentials. This is with the header Authorization.
In http://localhost:8001/swagger.json or http://localhost:8001/swagger/?format=openapi you can download the json and
next open in https://editor.swagger.io/
Notes: https://drf-yasg.readthedocs.io/en/latest/readme.html
, https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#infoObject
In the root folder the file "swagger-file" with last json.