# Todo App Frontend

A simple, modern web frontend for the Todo API.

## Features

- 🔐 User authentication (Login/Signup)
- ✅ Add, view, update, and delete todos
- 🎨 Modern, responsive UI
- 🔒 JWT token-based authentication
- 💾 Local storage for session persistence

## How to Use

### Option 1: Open in Browser (Simple)

1. Make sure your FastAPI backend is running on `http://localhost:8000`
2. Open `frontend/index.html` in your web browser
3. Create an account or login
4. Start managing your todos!

### Option 2: Using a Simple HTTP Server

If you get CORS errors, use a local server:

```bash
# Python 3
python -m http.server 8080 --directory frontend

# Or Node.js (if you have it)
npx serve frontend
```

Then open `http://localhost:8080` in your browser.

## Features

- **Authentication**: Sign up and login with email and password
- **Todo Management**: Add, complete, and delete todos
- **Secure**: Uses JWT tokens for authentication
- **Responsive**: Works on desktop and mobile devices

## API Endpoints Used

- `POST /signup` - Create new user account
- `POST /login` - Get authentication token
- `GET /todos` - Get all todos for logged-in user
- `POST /todos` - Create a new todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

## Customization

You can easily customize the styling by modifying the CSS in the `<style>` section of `index.html`.

## Technologies

- Pure HTML, CSS, and JavaScript (no frameworks)
- Fetch API for HTTP requests
- LocalStorage for token persistence

