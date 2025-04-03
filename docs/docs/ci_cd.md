# CI/CD

GitHub Actions is used for continuous integration and deployment.

## GitHub Actions Workflow

- Builds Docker images for test and production environments.
- Runs unit tests with coverage reporting (commented because of error 137 -not enough memory).

## Branches

- `main`: Main branch, protected by default.
- `develop`: Development branch, protected by default.

## Environments

- `dev`: Development environment.
- `prod`: Production environment. The main branch will be deployed there.

## Web deployment

We use [Render](https://render.com/) for web deployment. For the moment, the production environment is not set up.
You can try it out the development environment [here](https://peaks.onrender.com/).

