# Personal Notes

## This document contains my notes and thoughts while working on this project.

I want to explain how I will approach this task, why I will approach it this way, and what I expect to achieve. I will also detail obstacles I may encounter and how I will overcome them.

## Initial obstacles

1. I work on the familly PC which is a Windows machine and Docker does not start (exit code 4294967295).
2. I need to update wsl.
3. I had to travel this weekend.

1) I purged everything.
2) I reinstalled wsl.
3) I'm back now !!

## Overall Plan

### Initialization

1. Create the branch *develop*.
2. Define the project structure.
3. Design the DB structure.
4. Create a virtual environment.
5. List the needed modules in requirements.txt.
6. Install these modules in the *venv*.
7. Create the local DB (postgres) server with pgAdmin.
8. Secure the DB.
9. Start Fastapi locally.
10. Create the DB Models.
11. Migrate the models to create the DB.
12. Configure pytest and pytest-asyncio with the IDE.
13. Use Test Driven Development (TDD) to create the API endpoints.
14. Create a Dockerfile.
15. Create a docker-compose.yml file.
16. Add Github actions.
17. Add a secret manager.
18. Add redis.
19. Add a web documentation.
20. Add a web interface.

### Previsional project structure
```
/peaks
    /src
        __init__.py
        main.py         # entry point of the application FastAPI
        api/            # endpoints and routes
        models/         # definition of SQLAlchemy models
        core/           # configuration, utilities, secret management
    /tests            # unit and asynchronous tests with pytest
    /docs             # documentation with MkDocs
    Dockerfile
    docker-compose.yml
    requirements.txt
    README.md
```

