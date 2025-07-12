#!/bin/sh
pip install -r requirements.txt
alembic -c alembic.ini revision --autogenerate -m "$1" 