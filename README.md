# Todo API (FastAPI + PostgreSQL)

Secure Todo API with JWT auth, built on FastAPI and SQLAlchemy, backed by PostgreSQL. Ships with Docker/Docker Compose and a simple HTML frontend in `frontend/`.

## Tech

- **FastAPI**, **SQLAlchemy**, **PostgreSQL**
- **JWT** auth (`python-jose`), **passlib[bcrypt]`
- **Uvicorn** for ASGI, optional **Docker**/**Compose**

## Project Structure

```
app/
  main.py           # FastAPI app, routes, CORS, serves frontend
  database.py       # SQLAlchemy engine + Session
  models.py         # SQLAlchemy models
  schemas.py        # Pydantic schemas
  crud.py           # Database operations
  security.py       # Password hashing + JWT
frontend/
  index.html        # Simple UI that talks to the API
Dockerfile
docker-compose.yml
requirements.txt
```

## Environment

Create a `.env` file in the project root.

For Docker Compose (service name `db`):
```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/fastapi_db
SECRET_KEY=change-me-in-production
```

For local (Postgres on your machine):
```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db
SECRET_KEY=change-me-in-production
```

## Run with Docker Compose (recommended)

```bash
docker compose up --build
```

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs` (Swagger) and `http://localhost:8000/redoc`
- Frontend: `http://localhost:8000/` (served from `frontend/index.html` if present) or `http://localhost:8000/static` for static files.

Hot-reload is enabled in the container. Code changes in this folder reflect inside the `web` service via the mounted volume.

## Run locally without Docker

Prereqs: Python 3.11+, running PostgreSQL.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Ensure .env is created as above and DB exists
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs`.

## Auth flow

- `POST /signup` accepts JSON with `email` and `password` and creates a user.
- `POST /login` expects form data per OAuth2 (fields: `username` = your email, `password`). Returns `{ access_token, token_type }`.
- For protected routes, send `Authorization: Bearer <access_token>` header.

## Endpoints (summary)

- `POST /signup` — create user
- `POST /login` — login, receive JWT token
- `GET /users/{user_id}` — fetch user by id
- `GET /todos` — list todos for current user (JWT)
- `POST /todos` — create todo (JWT)
- `GET /todos/{todo_id}` — get a todo (JWT, owner only)
- `PUT /todos/{todo_id}` — update todo (JWT, owner only)
- `DELETE /todos/{todo_id}` — delete todo (JWT, owner only)

Open API docs at `/docs` for full request/response schemas.

## CORS

Development allows all origins. For production, restrict `allow_origins` in `app.main` to your domains.

## Frontend

A simple HTML frontend lives in `frontend/`. With Docker/Compose or `uvicorn`, it is served at `/` if `frontend/index.html` exists. You can also open it directly or serve it via:
Just visit `http://localhost:8000/` once the backend is running.

