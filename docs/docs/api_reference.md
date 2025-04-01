## API Reference

This section documents the API endpoints and their parameters, reflecting the current implementation using FastAPI and SQLModel.

### Endpoints

- **`GET /peaks/peak/{peak_id}`:** Retrieve a peak by its ID.
  - Parameters:
    - `peak_id` (path parameter): Integer, the ID of the peak to retrieve.
  - Response:
    - Returns a JSON representation of the `Peak` object.
    - Returns a 404 error if the peak is not found.
  - Example: `GET /peaks/peak/1`

- **`POST /peaks/peak/create`:** Create a new peak.
  - Request Body:
    - JSON representation of the `Peak` object (name, latitude, longitude, altitude).
  - Response:
    - Returns a JSON representation of the created `Peak` object.
    - Returns a 201 status code upon successful creation.
    - Returns a 400 error if there is an issue with the creation.
  - Example: `POST /peaks/peak/create` with JSON payload.

- **`POST /peaks/create`:** Bulk create peaks from a list.
  - Request Body:
    - JSON array of `Peak` objects.
  - Response:
    - Returns a 201 status code upon successful creation.
    - Returns a 400 error if there is an issue with the bulk creation.
  - Example: `POST /peaks/create` with JSON array payload.

- **`PUT /peaks/peak/{peak_id}`:** Update a peak by its ID.
  - Parameters:
    - `peak_id` (path parameter): Integer, the ID of the peak to update.
  - Request Body:
    - JSON representation of the `Peak` object with updated fields.
  - Response:
    - Returns a 200 status code upon successful update.
    - Returns a 404 error if the peak is not found.
  - Example: `PUT /peaks/peak/1` with JSON payload.

- **`DELETE /peaks/peak/{peak_id}`:** Delete a peak by its ID.
  - Parameters:
    - `peak_id` (path parameter): Integer, the ID of the peak to delete.
  - Response:
    - Returns a 204 status code upon successful deletion.
    - Returns a 404 error if the peak is not found.
  - Example: `DELETE /peaks/peak/1`

- **`GET /peaks/boundingbox`:** Retrieve peaks within a given geographical bounding box.
  - Query Parameters:
    - `min_lat` (float): Minimum latitude.
    - `max_lat` (float): Maximum latitude.
    - `min_lon` (float): Minimum longitude.
    - `max_lon` (float): Maximum longitude.
  - Response:
    - Returns a JSON array of `Peak` objects within the bounding box.
    - Returns a 404 error if no peaks are found.
  - Example: `GET /peaks/boundingbox?min_lat=44.5&max_lat=46.5&min_lon=5.5&max_lon=7.5`

### Data Models

- **Peak:**
  - `id`: Integer (auto-incrementing)
  - `name`: String
  - `lat`: Float
  - `lon`: Float
  - `altitude`: Float

### Dependencies

- `db: Session = Depends(get_db)`: Injects a database session into each endpoint.

### Error Handling

- Endpoints raise `HTTPException` with appropriate status codes (404, 400) and error details when necessary.
- Database transactions are rolled back in case of errors to maintain data integrity.
