# The Mountain Peaks API Documentation V1

This documentation provides a comprehensive guide to the Peaks API project, a simple web service for storing and retrieving mountain peaks data.

## Table of Contents

- [Home](index.md)
- ***[Try Out Now](https://peaks.onrender.com/auth/login)***
- [API Reference](api_reference.md)
- [Database](database.md)
- [Configuration](configuration.md)
- [CI/CD](ci_cd.md)
- [Security](security.md)

## Home

This documentation is accessible online, [here](https://peaks.onrender.com/).
The API is currently running in a development environment.

1. Open the [web page of the documentation](https://peaks.onrender.com/).
2. Click on ***Try Out Now*** in the summary to authenticate.
3. Land on the list of all peaks that are currently stored in the database.

Welcome to the Mountain Peaks API documentation. This API allows you to manage mountain peak data, including creating, reading, updating, and deleting peak records, as well as retrieving peaks within a specified geographical bounding box.

This project is built using:

- **FastAPI:** For the asynchronous REST API.
- **SQLAlchemy:** For database interaction.
- **Alembic:** For database migrations.
- **PostgreSQL:** As the database backend.
- **Docker & Docker Compose:** For containerization and deployment.
- **GitHub Actions:** For continuous integration and deployment.
- **MkDocs:** For the web documentation.

## Try it out

Connect to try it out **online**. Click ***[HERE](https://peaks.onrender.com/auth/login)***

### Prerequisites

- Python > 3.11
- Docker and Docker Compose installed.
- Postman or `curl` for testing API endpoints.

### Running the API

1. Clone the repository:

    ```bash
    git clone [https://github.com/nojoven/peaks.git](https://github.com/nojoven/peaks.git)
    cd peaks
    ```

2. Complete the `.env` file with the required environment variables.

3. Start the containers:

    ```bash
    docker-compose up --build
    ```

4. The API will be available at `http://localhost:8000`.

### Example Requests

- **Create a Peak:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{
      "name": "Mont Blanc",
      "latitude": 45.8326,
      "longitude": 6.8652,
      "altitude": 4808.73
    }' http://localhost:8000/peaks/create
    ```

- **Get a Peak:**

    ```bash
    curl http://localhost:8000/peaks/peak/1
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


## Unit tests

We use pytest for unit testing. If you want to run the tests locally, you can use the following command:

```bash
pytest --cov=src --cov-report=term-missing tests/ -v
```

You will need a python virtual environment to do so:

1. At the root of the project, run:

    ```bash
    python -m venv .venv
    ```

2. Activate the virtual environment:

    ```bash
    source .venv/bin/activate # or .venv\Scripts\activate on Windows
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the tests:

    ```bash
    pytest --cov=src --cov-report=term-missing tests/ -v
    ```

## MkDocs local documentation in your browser

You will need an activated python virtual environment as well. Please see the previous section. Then, follow these steps:

1. At the root of the project, run:

    ```bash
    mkdocs build --clean
    ```

2. Run

    ```bash
    mkdocs serve
    ```


## Follow us on **[GitHub](https://github.com/nojoven/peaks)**
