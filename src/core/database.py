# src/core/database.py

import logging
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

# Load environment variables
load_dotenv()
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


# Connection string
DATABASE_URL = f"{DATABASE_ENGINE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_ADDRESS}:{DATABASE_PORT}/{DATABASE_NAME}"


# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create database
def create_db():
    SQLModel.metadata.create_all(engine)

# Get session DB
def get_db() -> Generator[Session, None, None]:
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logging.error("Error during DB session usage: %s", e)
        raise
