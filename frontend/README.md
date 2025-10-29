# Todo App Frontend

A simple, modern web frontend for the Todo API.

## Features

- 🔐 Authentication (Signup/Login)
- ✅ Add, view, update, and delete todos
- 🔒 JWT bearer token stored in LocalStorage
- 🎨 Responsive UI

## How to Run

The backend can serve this page at `/` automatically when running with Docker or `uvicorn`.

- Start backend (Docker): `docker compose up`
- Visit: `http://localhost:8000/`

## API Endpoints Used

- `POST /signup` — Create a new user. Body: `{ "email", "password" }`
- `POST /login` — OAuth2 form body: `username=<email>&password=<password>` → `{ access_token }`
- `GET /todos` — Get todos for the logged-in user (requires `Authorization: Bearer <token>`)
- `POST /todos` — Create a todo (JWT)
- `PUT /todos/{id}` — Update a todo (JWT)
- `DELETE /todos/{id}` — Delete a todo (JWT)

## Configuration

If the backend is not on `http://localhost:8000`, edit the API base URL inside `frontend/index.html`.

## Customize

Tweak styles inside the `<style>` tag in `index.html`. The frontend uses plain HTML/CSS/JS with the Fetch API and LocalStorage.

