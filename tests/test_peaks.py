import json
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, SQLModel, select
from src.main import app
from src.core.database import engine, get_db
from src.models.peak import Peak
from tests.tests_helpers import create_peak_data


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
    peak_data = create_peak_data()

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
    peak_data = create_peak_data()

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
    peak_data = create_peak_data()

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
    assert update_response.status_code == 200


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


@pytest.mark.asyncio
async def test_delete_peak(client):
    """Test the deletion of a Peak via the API."""
    peak_data = create_peak_data()

    # First, create a peak
    create_response = client.post("/peaks/peak/create", json=peak_data)
    assert create_response.status_code == 201
    created_data = create_response.json()
    peak_id = created_data["id"]

    # Now, delete the peak
    delete_response = client.delete(f"/peaks/peak/{peak_id}")
    assert delete_response.status_code == 204

    # Now, try to delete a peak that does not exist
    not_found_delete_response = client.delete(f"/peaks/peak/{peak_id+1}")
    assert not_found_delete_response.status_code == 404
    assert not_found_delete_response.json()["detail"] == "Peak not found"

    # Ensure the peak is deleted from the database
    with Session(engine) as db:
        peak_in_db = db.exec(select(Peak).where(Peak.id == peak_id)).first()
        assert peak_in_db is None  # Peak should no longer exist


@pytest.fixture
def get_peaks_list():
    with open("tests/peaks_list.json", "r") as f:
        peaks_list = json.load(f)
        assert isinstance(peaks_list, list), "Peaks list should be a list"
        assert len(peaks_list) > 0, "Peaks list should not be empty"
    return peaks_list

@pytest.mark.asyncio
async def test_bulk_create_peaks(client, get_peaks_list):
    """
    Test the bulk creation of peaks via the API.
    """
    input_count = len(get_peaks_list)

    response = client.post("/peaks/create", json=get_peaks_list)
    assert response.status_code == 201, "Bulk creation should return 201 status"
    assert response.content.decode() == "Peaks were inserted successfully", "Check if insertion success message is correct"
    
    
 
    # Verify each created peak has an auto-generated ID
    with Session(engine) as db:
        # Get all inserted peaks
        bulk_insert_result = db.exec(select(Peak))
        inserted_peaks = bulk_insert_result.all()
        #
        assert len(inserted_peaks) == input_count, f"Inserted ({len(inserted_peaks)}) elements should be equal to ({input_count})"
        
        #
        for peak_data in get_peaks_list:
            peak = db.exec(select(Peak).where(Peak.name == peak_data["name"])).first()
            assert peak is not None, f"Peak with name {peak_data['name']} should exist in the database"
            assert peak.name == peak_data["name"], f"Peak name mismatch: expected {peak_data['name']}, found {peak.name}"
            assert peak.lat == peak_data["lat"], f"Peak latitude mismatch: expected {peak_data['lat']}, found {peak.lat}"
            assert peak.lon == peak_data["lon"], f"Peak longitude mismatch: expected {peak_data['lon']}, found {peak.lon}"
            assert peak.altitude == peak_data["altitude"], f"Peak altitude mismatch: expected {peak_data['altitude']}, found {peak.altitude}"

    # Cleanup: Delete the peaks after the test to ensure no pollution in the database
    with Session(engine) as db:
        for peak_element in get_peaks_list:
            peak = db.exec(select(Peak).where(Peak.name == peak_element["name"])).first()
            if peak:
                db.delete(peak)
        db.commit()

    # Check that the table is empty after the deletion
    with Session(engine) as db:
        remaining_peaks = db.exec(select(Peak)).all()
        assert len(remaining_peaks) == 0, "The Peak table should be empty after cleanup"


@pytest.mark.asyncio
async def test_get_peaks_in_bounding_box(client, get_peaks_list):
    """Test the retrieval of peaks within a bounding box."""

    bulk_response = client.post("/peaks/create", json=get_peaks_list)
    assert bulk_response.status_code == 201, "Bulk creation should return 201 status"
    assert bulk_response.content.decode() == "Peaks were inserted successfully", "Bulk insertion message mismatch"

    # Define the bounding box coordinates
    bounding_box_coords = {
        "min_lat": 45.8,
        "max_lat": 46.0,
        "min_lon": 6.8,
        "max_lon": 7.9
    }
    
    # Perform the request to get peaks within the bounding box
    get_response = client.get("/peaks/boundingbox", params=bounding_box_coords)
    filtered_peaks = get_response.json()
    expected_count = 2

    # Assert the response status code is 200 OK
    assert get_response.status_code == 200
    # Assert the response is a list of peaks
    assert isinstance(filtered_peaks, list), "Response should be a list of peaks"
    # Assert the number of peaks in the bounding box is correct
    assert len(filtered_peaks) == expected_count, f"Expected {expected_count} peaks in bounding box, got {len(filtered_peaks)}"
    
    # Clean up the database after the test
    with Session(engine) as db:
        for peak in get_peaks_list:
            db.exec(delete(Peak).where(Peak.name == peak["name"]))
        db.commit()

    # Ensure the table is empty after cleanup
    with Session(engine) as db:
        remaining_peaks = db.exec(select(Peak)).all()
        assert len(remaining_peaks) == 0, "The Peak table should be empty after cleanup"

