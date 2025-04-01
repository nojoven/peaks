# src/core/database.py

import logging
from src.core.db_helpers import get_db_url
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

# Load environment variables
load_dotenv()

# Create engine
engine = create_engine(get_db_url(), echo=True)

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
