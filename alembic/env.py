import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# load .env
from dotenv import load_dotenv
load_dotenv()

# import your SQLAlchemy models
from app.db.models import Base  # Make sure Base.metadata includes all models

# Alembic Config object
config = context.config

# override the URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

# Setup logging
fileConfig(config.config_file_name)

# target_metadata is your models' metadata
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
