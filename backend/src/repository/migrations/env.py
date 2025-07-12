import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.pool import NullPool as SQLAlchemyNullPool
from sqlalchemy import create_engine

from src.repository.table import Base
from src.models.db.event import Event, KudagoEvent

from dotenv import load_dotenv
import os
import sys
# Удалены все print и sys.path.append для чистоты
load_dotenv()

from alembic import context
config = context.config
# db_url = os.environ["DATABASE_URL"].replace("+asyncpg", "+psycopg2")
# if "?" in db_url:
#     db_url += "&client_encoding=utf8"
# else:
#     db_url += "?client_encoding=utf8"
# config.set_main_option("sqlalchemy.url", db_url)
# print("DATABASE_URL (for alembic):", db_url)
# print("alembic.ini sqlalchemy.url:", config.get_main_option("sqlalchemy.url"))

target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    if url is None:
        raise RuntimeError("No sqlalchemy.url found in config")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = config.get_main_option("sqlalchemy.url")
    if url is None:
        raise RuntimeError("No sqlalchemy.url found in config")
    connectable = create_engine(
        url,
        poolclass=SQLAlchemyNullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
