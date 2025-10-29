"""FastAPI application entry point."""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from pathlib import Path
from app.database import Base, engine
from app.dependencies import get_db, get_current_user, oauth2_scheme
from app import crud, schemas, models
from app.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# Create tables if not already present (for first-time local runs)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API with Users")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Serve the frontend at root
@app.get("/")
async def read_root():
    """Serve the frontend HTML file."""
    frontend_file = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_file.exists():
        return FileResponse(frontend_file)
    return {"message": "Frontend not found. API is running. Visit /docs for API documentation."}

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon if it exists."""
    favicon_file = Path(__file__).parent.parent / "frontend" / "favicon.ico"
    if favicon_file.exists():
        return FileResponse(favicon_file)
    return {"detail": "Not found"}


# -------------------------------
# AUTH ROUTES
# -------------------------------


@app.post("/signup", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **email**: User's email address (must be unique)
    - **password**: User's password (will be hashed)
    """
    # Check if email already exists
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return crud.create_user(db=db, user=user)


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login and receive an access token.
    
    - **username**: Your email address (use username field)
    - **password**: Your password
    
    Returns a JWT access token for authenticated requests.
    Note: OAuth2 standard uses "username" field name, but it accepts your email address.
    """
    # OAuth2PasswordRequestForm uses 'username' field, but we treat it as email
    email = form_data.username
    password = form_data.password

    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# -------------------------------
# USER ROUTES
# -------------------------------


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.
    
    Returns user details including associated todos.
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------------------------------
# TODO ROUTES (Require JWT Authentication)
# -------------------------------


@app.post("/todos", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: schemas.TodoCreateAuth,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new todo for the authenticated user.
    
    Requires bearer token authentication.
    
    - **title**: Todo title
    - **description**: Optional todo description
    - **completed**: Completion status (default: False)
    """
    # Create todo with current user's ID
    todo_with_user = schemas.TodoCreate(**todo.dict(), user_id=current_user.id)
    return crud.create_todo(db=db, todo=todo_with_user)


@app.get("/todos", response_model=list[schemas.Todo])
def get_todos(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all todos for the authenticated user.
    
    Requires bearer token authentication.
    Returns a list of todos belonging to the authenticated user.
    """
    return crud.get_todos_by_user(db, user_id=current_user.id)


@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def get_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a single todo by ID (only if owned by authenticated user).
    
    Requires bearer token authentication.
    Returns detailed information about a specific todo.
    """
    todo = crud.get_todo(db, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Verify todo belongs to current user
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")
    
    return todo


@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(
    todo_id: int,
    todo_update: schemas.TodoCreateAuth,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing todo by ID (only if owned by authenticated user).
    
    Requires bearer token authentication.
    Updates the todo with the provided information.
    """
    todo = crud.get_todo(db, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Verify todo belongs to current user
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    
    # Create update schema with user_id
    todo_with_user = schemas.TodoCreate(**todo_update.dict(), user_id=current_user.id)
    return crud.update_todo(db=db, todo_id=todo_id, todo_update=todo_with_user)


@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a todo by ID (only if owned by authenticated user).
    
    Requires bearer token authentication.
    Permanently removes the specified todo from the database.
    """
    todo = crud.get_todo(db, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Verify todo belongs to current user
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")
    
    crud.delete_todo(db=db, todo_id=todo_id)
    return {"message": "Todo deleted successfully"}