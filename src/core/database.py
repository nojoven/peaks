# src/core/database.py

import logging
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

# Load environment variables
load_dotenv()

# Connection string
DATABASE_URL = os.getenv("DEFAULT_DB_URL", None)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create database
def create_db():
    SQLModel.metadata.create_all(engine)

# Get session DB
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logging.error("Error during DB session usage: %s", e)
            raise
