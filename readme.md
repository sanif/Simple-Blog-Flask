# Simple Blog APIs in Flask

[![The MIT License](https://img.shields.io/badge/license-MIT-orange.svg?style=flat-square)](LICENSE)


This app is hosted at https://sanif-simple-blog-flask.herokuapp.com/

## Admin Panel
https://sanif-simple-blog-flask.herokuapp.com/admin

## Swagger/OpenApi
https://sanif-simple-blog-flask.herokuapp.com/api/v2

## Getting Started

### Prerequisites

- Python 3.9.2 or higher

### Project setup
```sh
# clone the repo
# move to the project folder
$ cd repo-folder
```

### Creating virtual environment

- Install `pipenv` a global python project `pip install pipenv`
- Create a `virtual environment` for this project
```shell
# creating pipenv environment for python 3
$ pipenv --three
# activating the pipenv environment
$ pipenv shell
# install all dependencies (include -d for installing dev dependencies)
$ pipenv install -d

# if you have multiple python 3 versions installed then
$ pipenv install -d --python 3.9
```
### Configuration

- There are 3 configurations `development`, `staging` and `production` in `config.py`. Default is `development`
- Create a `.env` file from `.env.example` and set appropriate environment variables before running the project

### Running app

- Run flask app `python run.py`
- Logs would be generated under `log` folder
- Run migrations using `flask db upgrade`


