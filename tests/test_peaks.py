import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, select
from src.main import app
from src.core.database import engine, get_db
from src.models.peak import Peak


# Use a test database (in-memory for example)
@pytest.fixture(name="session")
def session_fixture():
    """Create a new database session for testing."""
    SQLModel.metadata.create_all(engine)  # Create tables
    with Session(engine) as session:
        yield session  # Provide session to tests
    SQLModel.metadata.drop_all(engine)  # Cleanup after tests

# Override FastAPI dependency injection to use test DB
@pytest.fixture(name="client")
def client_fixture(session):
    """Create a test client with the overridden DB session."""
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# Test creating a Peak
@pytest.mark.asyncio
async def test_create_peak(client):
    """Test the creation of a Peak via the API."""
    peak_data = {
        "name": "Mont Blanc",
        "lat": 45.8325,
        "lon": 6.8650,
        "altitude": 4808
    }

    response = client.post("/peaks/peak/create", json=peak_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Mont Blanc"
    assert data["lat"] == 45.8325
    assert data["lon"] == 6.8650
    assert data["altitude"] == 4808
    assert "id" in data  # The ID should be auto-generated


# Verify that the Peak exists in the database
    with Session(engine) as db:
        peak_in_db = db.exec(select(Peak).where(Peak.id == data["id"])).first()
        assert peak_in_db is not None
        assert peak_in_db.name == peak_data["name"]
        assert peak_in_db.lat == peak_data["lat"]
        assert peak_in_db.lon == peak_data["lon"]
        assert peak_in_db.altitude == peak_data["altitude"]

        # Deleting the Peak from the database to clean up
        db.delete(peak_in_db)
        db.commit()  # Ensure the delete is committed



@pytest.mark.asyncio
async def test_create_peak_missing_name(client):
    """Test that invalid data returns an error."""
    # Sending a peak with invalid data (e.g., missing 'name')
    response = client.post(
        "/peaks/peak/create",
        json={"lat": 45.0, "lon": 7.0, "altitude": 1000}
    )

    # Check that the response status code is 400 (bad request)
    assert response.status_code == 400
    # Fetch the response JSON
    error_response = response.json()
    print(error_response)
    # Check that the error message contains the 'detail' field
    assert "detail" in error_response, "Error response should contain 'detail'"

    # Check if the error message contains a relevant message about the missing 'name'
    assert "psycopg.errors.NotNullViolation" in error_response["detail"]




@pytest.mark.asyncio
async def test_read_peak(client):
    """Test the creation of a Peak via the API."""
    peak_data = {
        "name": "Mont Blanc",
        "lat": 45.8325,
        "lon": 6.8650,
        "altitude": 4808
    }

    create_response = client.post("/peaks/peak/create", json=peak_data)    
    created_data = create_response.json()
    peak_id = created_data["id"]
    
    read_response = client.get(f"/peaks/peak/{peak_id}")
    assert read_response.status_code == 200
    read_data = read_response.json()
    assert read_data["id"] == peak_id
    assert read_data["name"] == peak_data["name"]
    assert read_data["lat"] == peak_data["lat"]
    assert read_data["lon"] == peak_data["lon"]
    assert read_data["altitude"] == peak_data["altitude"]
    
    not_found_response = client.get("/peaks/peak/999999999")
    assert not_found_response.status_code == 404


# Verify that the Peak exists in the database
    with Session(engine) as db:
        peak_in_db = db.exec(select(Peak).where(Peak.id == peak_id)).first()
        # Deleting the Peak from the database to clean up
        db.delete(peak_in_db)
        db.commit()  # Ensure the delete is committed



@pytest.mark.asyncio
async def test_update_peak(client):
    """Test the updating of a Peak via the API."""
    peak_data = {
        "name": "Mont Blanc",
        "lat": 45.8325,
        "lon": 6.8650,
        "altitude": 4808
    }

    # First, create a peak
    create_response = client.post("/peaks/peak/create", json=peak_data)
    assert create_response.status_code == 201
    created_data = create_response.json()
    peak_id = created_data["id"]

    # Now, update the peak
    updated_data = {
        "name": "Mont Blanc Updated",
        "lat": 45.0,
        "lon": 7.0,
        "altitude": 5000
    }

    update_response = client.put(f"/peaks/peak/{peak_id}", json=updated_data)
    assert update_response.status_code == 204


    # Check that the updated data is returned correctly
    with Session(engine) as db:
        peak_in_db = db.exec(select(Peak).where(Peak.id == peak_id)).first()
        assert peak_in_db is not None
        assert peak_in_db.name == "Mont Blanc Updated"
        assert peak_in_db.lat == 45.0
        assert peak_in_db.lon == 7.0
        assert peak_in_db.altitude == 5000

    # Deleting the Peak from the database to clean up
    with Session(engine) as db:
        peak_in_db = db.exec(select(Peak).where(Peak.id == peak_id)).first()
        db.delete(peak_in_db)
        db.commit()  # Ensure the delete is committed

