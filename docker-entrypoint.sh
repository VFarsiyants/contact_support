#!/bin/sh

echo "Running migrations"
alembic upgrade head

# start bot
python main.py
