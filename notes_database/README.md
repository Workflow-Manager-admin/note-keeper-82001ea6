# notes_database

This is the PostgreSQL container for the notes application. It stores users and notes persistently, and is intended for use by the FastAPI backend.

## Usage

- The database starts with these default credentials:
  - `POSTGRES_DB: notes_app`
  - `POSTGRES_USER: notes_user`
  - `POSTGRES_PASSWORD: notes_pass`
- The server runs on port `5432` (exposed).
- The DB schema initializes automatically via `/docker-entrypoint-initdb.d/init.sql`.

## Backend Integration

Set the `DATABASE_URL` environment variable in your backend's `.env` like:

```
DATABASE_URL=postgresql+psycopg2://notes_user:notes_pass@notes_db:5432/notes_app
```

While running locally (if using host networking), use:

```
DATABASE_URL=postgresql+psycopg2://notes_user:notes_pass@localhost:5432/notes_app
```

The backend expects two tables:
- `users`: for user authentication.
- `notes`: for storing notes with FK to `users`.

## Volumes

- Persistent storage: `db_data` docker volume.

## Health Check

You can check database connectivity by connecting using psql or pg_isready.

```
docker exec -it notes_db psql -U notes_user -d notes_app
```
