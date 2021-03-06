import pathlib
import sys
import alembic
from sqlalchemy import engine_from_config, pool

from logging.config import fileConfig
import logging

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import DATABASE_URL

config = alembic.context.config

fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.ini")


def run_migrations_online() -> None:
    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", str(DATABASE_URL))

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(
            connection=connection,
            target_metadata=None
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    alembic.context.configure(url=str(DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running offline migration")
    run_migrations_offline()
else:
    logger.info("Running online migration")
    run_migrations_online()