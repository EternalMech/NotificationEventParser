#!/bin/sh
pip install -r requirements.txt
alembic -c alembic.ini upgrade head 