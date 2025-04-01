## Database

The API uses a PostgreSQL database to store peak data.

### Database Schema

- **`peaks` table:**
  - `id` (SERIAL PRIMARY KEY)
  - `name` (VARCHAR)
  - `latitude` (FLOAT)
  - `longitude` (FLOAT)
  - `altitude` (FLOAT)

  ### Database Migrations

Alembic is used for database migrations.


### Environment Variables

- `DATABASE_URL`: PostgreSQL database connection URL.
