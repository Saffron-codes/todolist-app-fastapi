# Frontend Options for Your Todo API

## Built-in API Documentation (FastAPI)

Your API comes with **automatic interactive documentation**:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These let you test your API directly from the browser without building a separate frontend!

## Custom Frontend

I've created a simple, beautiful frontend for you in the `frontend/` folder.

### Quick Start

1. **Start your API** (if not already running):
   ```bash
   docker compose up
   ```

2. **Open the frontend**:
   - Simply open `frontend/index.html` in your browser, OR
   - For best results, use a local server:
     ```bash
     python -m http.server 8080 --directory frontend
     ```
     Then visit http://localhost:8080

3. **Sign up and start creating todos!**

### Features

✅ User authentication (Login/Signup)  
✅ Create, view, update, and delete todos  
✅ Modern, responsive UI  
✅ JWT token authentication  
✅ Session persistence (stays logged in)  

### API + Frontend Architecture

```
┌─────────────┐         HTTP + JWT         ┌──────────────┐
│   Browser   │ ──────────────────────────> │  FastAPI     │
│  (Frontend) │                             │  (Backend)   │
└─────────────┘ <────────────────────────── └──────────────┘
               JSON + Bearer Token
```

## Alternative Frontend Frameworks

If you want to use a modern framework:

### React + TypeScript

```bash
npx create-react-app my-todo-app --template typescript
cd my-todo-app
npm install axios
```

### Vue.js

```bash
npm create vue@latest my-todo-app
cd my-todo-app
npm install axios
```

### Next.js

```bash
npx create-next-app@latest my-todo-app
cd my-todo-app
```

## Using the Provided Frontend

The frontend in `frontend/index.html` is:
- **XML**: No build step required
- **Modern**: Uses fetch API and modern JavaScript
- **Complete**: Has all CRUD operations for todos
- **Styled**: Beautiful gradient UI with animations

Just open it in your browser and start using it!

## Important: CORS

CORS has been enabled in your FastAPI app to allow the frontend to make requests. The configuration is in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For production**, change `allow_origins=["*"]` to specific domains like:
```python
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
```

