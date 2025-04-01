# The Mountain Peaks API Documentation V1

This documentation provides a comprehensive guide to the Peaks API project, a simple web service for storing and retrieving mountain peaks data.

## Table of Contents

- [Home](index.md)
- [Try it out](http://127.0.0.1:8000/auth/login)
- [API Reference](api_reference.md)
- [Database](database.md)
- [Configuration](configuration.md)
- [CI/CD](ci_cd.md)
- [Security](security.md)

## Home

Welcome to the Mountain Peaks API documentation. This API allows you to manage mountain peak data, including creating, reading, updating, and deleting peak records, as well as retrieving peaks within a specified geographical bounding box.

This project is built using:

- **FastAPI:** For the asynchronous REST API.
- **SQLAlchemy:** For database interaction.
- **Alembic:** For database migrations.
- **PostgreSQL:** As the database backend.
- **Docker & Docker Compose:** For containerization and deployment.
- **GitHub Actions:** For continuous integration and deployment.

## Try it out

Connect to try it out.


### Prerequisites

- Docker and Docker Compose installed.
- Postman or `curl` for testing API endpoints.

### Running the API

1. Clone the repository:

    ```bash
    git clone [https://github.com/nojoven/peaks.git](https://github.com/nojoven/peaks.git)
    cd peaks
    ```

2. Start the containers:

    ```bash
    docker-compose up --build
    ```

3. The API will be available at `http://localhost:8000`.

### Example Requests

- **Create a Peak:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{
      "name": "Mont Blanc",
      "latitude": 45.8326,
      "longitude": 6.8652,
      "altitude": 4808.73
    }' http://localhost:8000/peaks/
    ```

- **Get a Peak:**

    ```bash
    curl http://localhost:8000/peaks/1
    ```

- **Get Peaks within a bounding box:**

    ```bash
    curl http://localhost:8000/peaks/?min_lat=44.5&max_lat=46.5&min_lon=5.5&max_lon=7.5
    ```



## To be added

- Authentication and authorization.
- Input validation and error handling.
- Detailed error messages.
- Secret management.
- Web interface.
- More comprehensive documentation.
- Add more tests.
- Add security measures.