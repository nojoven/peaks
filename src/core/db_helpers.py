import os
from alembic import context

def get_db_url():
    """
    Generates a database connection URL based on environment variables.
    Args: None
    Returns:
        str: A formatted database connection URL.
    Raises:
        ValueError: If any of the required environment variables is not set.
    """
    DATABASE_ENGINE = os.getenv("DATABASE_ENGINE")
    if not DATABASE_ENGINE:
        raise ValueError("DATABASE_ENGINE is not set in the environment variables.")

    DATABASE_USER = os.getenv("POSTGRES_USER")
    if not DATABASE_USER:
        raise ValueError("DATABASE_USER is not set in the environment variables.")

    DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    if not DATABASE_PASSWORD:
        raise ValueError("DATABASE_PASSWORD is not set in the environment variables.")

    DATABASE_ADDRESS = os.getenv("DATABASE_ADDRESS")
    if not DATABASE_ADDRESS:
        raise ValueError("DATABASE_ADDRESS is not set in the environment variables.")

    DATABASE_PORT = os.getenv("DATABASE_PORT")
    if not DATABASE_PORT:
        raise ValueError("DATABASE_PORT is not set in the environment variables.")

    DATABASE_NAME = os.getenv("DATABASE_NAME")
    if not DATABASE_NAME:
        raise ValueError("DATABASE_NAME is not set in the environment variables.")

    # Connection string
    db_connection_string = f"{DATABASE_ENGINE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_ADDRESS}:{DATABASE_PORT}/{DATABASE_NAME}"
    return db_connection_string