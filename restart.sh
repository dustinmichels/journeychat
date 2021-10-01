#! /usr/bin/env bash

# remove old stuff
rm journeychat.db
rm -rf alembic/versions/*

# Let the DB start
python ./journeychat/backend_pre_start.py

# autogenerate versions
alembic revision --autogenerate -m "Add tables"

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./journeychat/initial_data.py