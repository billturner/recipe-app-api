# recipe-app-api

**To run the tests and linter via docker**

```bash
docker-compose run app sh -c "python manage.py test && flake8"
```

**Adding a new app to the project**

```bash
docker-compose run --rm app sh -c "python manage.py startapp appname"
```

**Start up the django app**

```bash
docker-compose up
```

**Create a new migration**

```bash
docker-compose run app sh -c "python manage.py makemigrations"
```
