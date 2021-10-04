#! /usr/bin/env bash

# Let the DB start
python ./journeychat/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./journeychat/initialize_data.py