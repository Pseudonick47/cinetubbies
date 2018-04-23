# cinetubbies
> Projekat iz ISA &amp; MRS

## Build Setup

### Docker
> django + mariadb
``` bash
# in the project root
docker-compose up
```

### Frontend - Vue.js
``` bash
# install dependencies
cd frontend
yarn install

# serve with hot reload at localhost:8080
yarn run dev

# build for production with minification
yarn run build

```
### Backend - Django
Note: Please keep virtualenvs outside of project directory.

``` bash
# install pipenv (with your package manager or pip)
yaourt -S python-pipenv
# or
sudo pip install pipenv

cd backend

# install all python dependencies
pipenv install

# to activate venv
pipenv shell

# run migrations
python manage.py migrate

# create superuser
python manage.py createsuperuser

# run development server with hot reload at localhost:8000
python manage.py runserver

# run development mail server
python -m smtpd -n -c DebuggingServer localhost:1025
# or use mailcatcher or similar service
```
