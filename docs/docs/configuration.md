
# Configuration

## Dockerfile

The Dockerfile is used to build the API container.

## Docker Compose

The docker-compose.yml file is used to define and run multi-container Docker applications.

## GitHub Actions

The .github/workflows/docker-compose-ci.yml file is used to define the CI/CD workflow.

## .env

We use a simple .env file to store the environment variables.

### Database

POSTGRES_USER
POSTGRES_PASSWORD
DATABASE_ENGINE
DATABASE_ADDRESS
DATABASE_NAME
DATABASE_PORT

### OAuth

OAUTH_GITHUB_CLIENT_ID
OAUTH_GITHUB_CLIENT_SECRET
OAUTH_GITHUB_ACCESS_TOKEN_URL
OAUTH_GITHUB_AUTHORIZE_URL
OAUTH_GITHUB_API_BASE_URL

### API

PEAK_API_SECRET_KEY
MANAGER_API_KEY

### Docker

DOCKER_COMPOSE_DATABASE_PORT

### Production

PRODUCTION = TRUE  or FALSE (default: FALSE)

### Sentry

SENTRY_DSN : URL of your Sentry project
