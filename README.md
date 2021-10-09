# Journey Chat

Backend for JourneyChat. Built with [FastAPI](https://fastapi.tiangolo.com/), in Python.

FastAPI creates and manages a SQL database using sqlalchemy for tracking key entities: rooms, messages, users.

- See `journeychat/models` for SQL models, and `journeychat/schemas` for their respective Pydantic models.
- Internal interface for modifying database data in `journeychat/crud`
- External interface (API) setup in `journeychat/api`.

There is great, auto-generated documentation at `localhost:8000/docs` when you run the program.

There is also a socketio server mounted as a sub-application of the main FastAPI app. See: `journeychat/socketio`.

When you run pre-start script below, database will be created and populated with some sample data. You should be able to login at the front-end, or within the interactive docs, for example, using:

```text
email: dustin@dustin.com
password: dustin
```

## Setup

[Install poetry](https://python-poetry.org/docs/#installation).

Install python dependencies:

```sh
poetry install
```

Run database setup script:

```sh
poetry run ./prestart.sh
```

## Run

```sh
poetry run ./run.sh
```
