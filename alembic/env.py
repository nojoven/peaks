
from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel, create_engine
from src.models.peak import Peak  # Import your models here
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Define the engine URL from the .env file or your settings
DATABASE_ENGINE = os.getenv("DATABASE_ENGINE")
if not DATABASE_ENGINE:
    raise ValueError("DATABASE_ENGINE is not set in the environment variables.")
DATABASE_USER = os.getenv("POSTGRES_USER")
if not DATABASE_USER:
    raise ValueError("DATABASE_USER is not set in the environment variables.")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
if not DATABASE_PASSWORD:
    raise ValueError("DATABASE_PASSWORD is not set in the environment variables.")
DATABASE_NAME = os.getenv("DATABASE_NAME")
if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME is not set in the environment variables.")
DATABASE_ADDRESS = os.getenv("DATABASE_ADDRESS")
if not DATABASE_ADDRESS:
    raise ValueError("DATABASE_ADDRESS is not set in the environment variables.")
DATABASE_PORT = os.getenv("DATABASE_PORT")
if not DATABASE_PORT:
    raise ValueError("DATABASE_PORT is not set in the environment variables.")


DATABASE_URL = f"{DATABASE_ENGINE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_ADDRESS}:{DATABASE_PORT}/{DATABASE_NAME}"

# Set the SQLAlchemy URL in Alembic config dynamically
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
