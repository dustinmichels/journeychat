# Journey Chat

## Usage

```sh
poetry run ./run.sh
```

## Setup

[Install poetry](https://python-poetry.org/docs/#installation).

Install python dependencies:

```sh
poetry install
```

Database changes:

```sh
alembic revision --autogenerate -m "Add user table"
```
