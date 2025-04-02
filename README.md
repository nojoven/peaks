[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/python-3.12.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/works-on-my-machine.svg)](https://forthebadge.com)
# Peaks 

A simple web service for storing and retrieving mountain peaks. This is a job application exercise.


## Expected results

###  Python

    - Fastapi framework and asynchronous programming
    - models/db tables for storing a peak location and attribute: lat, lon, altitude, name
    - REST API endpoints to :
    - Create/read/update/delete a peak
    - Retrieve a list of peaks in a given geographical bounding box
    - An API documentation page
    - As many functions as possible should be tested (coverage > 90 %)

### Docker

    - This app should be deployable in Docker and Docker Compose.
    - Optional: Secrets must be kept safe and secure

### CI/CD

    - Github action: CI has to be implemented to build docker images in test and production environments

## Analysis

### Expected software

#### Web API

    - Python REST API with Fastapi
    - Asynchronous programming skills should be demonstrated
    - At least one database should be used
    - The database will store peaks with attributes: lat, lon, altitude, name
    - Create a peak
    - Read a peak
    - Update a peak
    - Delete a  peak
    - Retrieve a list of peaks in a given geographical bounding box knowing that a bounding box is defined by:

        - Minimum latitude (bottom)
        - Maximum latitude (top)
        - Minimum longitude (left)
        - Maximum longitude (right)
        - For example, in the French Alps:
        - Min latitude: 44.5°N
        - Max latitude: 46.5°N
        - Min longitude: 5.5°E
        - Max longitude: 7.5°E

    - API documentation page (e.g. Swagger)
    - Unit tests with coverage > 90 %

#### Portability

    - Docker (Dockerfile) to :
        - Create and build images
        - Run the application
    - Docker Compose (docker-compose.yml)

#### Security

    - A secret manager should be used to store sensitive data

#### Continuous Integration/Continuous Deployment (CI/CD)

    - Github action has to be added and configured
    - This means at least 2 branches: main and develop

## Insights

We can deduce the following:

### Coding

1. A Python environment is required
2. Multiple additional Python modules are needed and we can use:

    - SQLAlchemy
    - Alembic
    - psycopg3
    - pytest
    - pytest-asyncio
    - pytest-cov
    - python-dotenv

3. No visual interface is listed in the requirements, however we can add one.
4. Same with authentication, authorizations, privileges, sessions, etc.
5. We are free to choose the appropriate serialization method.
6. Except for the secret manager, other security measures are optional.
7. Postman will be used to test the HTTP requests.

### Database

- A database is required and we are free to choose the appropriate one.

### Containers

There will be at least 3 containers:

    - Application
    - Database
    - Web server
If implemented, the secret manager should have its own container.
**So, ideally we'll have at least 4 containers.**

### Documentation

A documentation page is required (e.g. Swagger). The good news is that Fastapi has a built-in documentation page. We'll use the default Swagger UI.

Additionnally, a web documentation is provided. 
