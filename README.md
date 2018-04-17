# cinetubbies
> Projekat iz ISA &amp; MRS

## Build Setup

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
# create virtualenv folder outside of project
mkdir ~/.virtualenvs
cd ~/.virtualenvs
virtualenv isa

# and new virtualenv
source ~/.virtualenvs/isa/bin/activate

cd backend

# install all python dependencies
pip install -r requirements

# run migrations
python manage.py migrate

# run development server with hot reload at localhost:8000
python manage.py runserver
```