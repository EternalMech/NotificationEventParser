#!/bin/sh
pip install -r requirements.txt
alembic -c backend/alembic.ini upgrade head 