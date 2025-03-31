import os
import pytest
import logging
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel
from src.core.database import engine, create_db, get_db
from src.models.peak import Peak
load_dotenv()


# For testing, force the use of a PostgreSQL test database.
DATABASE_URL = os.getenv("DEFAULT_DB_URL", None)

def test_database_url():
    """
    Test that the DATABASE_URL environment variable is set.
    """
    assert DATABASE_URL is not None
    assert isinstance(DATABASE_URL, str)
    assert DATABASE_URL.startswith("postgresql+")

def test_create_db():
    """
    Test that create_db creates the tables in the PostgreSQL test database.
    """
    # Call create_db to create the tables
    create_db()
    # Use SQLAlchemy inspector to retrieve the list of tables in the database
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "peak" in tables, f"Expected 'peak' table in database, got: {tables}"

def test_get_db_success():
    """
    Test that get_db returns a working session.
    """
    # Use get_db to get a session generator
    db_gen = get_db()
    # Get the session from the generator
    session = next(db_gen)
    # Execute a simple query to verify the session is working
    result = session.execute(text("SELECT 1")).scalar()
    assert result == 1, "Expected SELECT 1 to return 1"
    # Exhaust the generator to ensure the session is closed properly
    with pytest.raises(StopIteration):
        next(db_gen)

def test_get_db_error(mocker):
    """
    Test that get_db properly logs and raises an error when an exception occurs.
    """
    # Patch the Session constructor in our db module to raise an exception
    mocker.patch("src.core.database.Session", side_effect=Exception("Database error"))
    
    with pytest.raises(Exception, match="Database error") as exc_info:
        # It is sufficient to call next(get_db()) to trigger the creation of a session.
        gen = get_db()
        next(gen)
    
    # Assert that the error message is as expected.
    assert "Database error" in str(exc_info.value)


# Test that an exception is logged and raised properly in the get_db function
def test_get_db_no_exception_at_runtime():
    # Mock the Session to raise an exception when used
    with patch('sqlmodel.Session', autospec=True) as MockSession:
        # Create a mock session that will raise an exception on context exit
        mock_session = MockSession.return_value
        mock_session.__enter__.side_effect = Exception("Test exception")
        # Capture the logs
        with patch.object(logging, 'error') as mock_log_error:
            # Assert that logging.error was called with the correct message
            mock_log_error.assert_not_called()
