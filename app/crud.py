"""Database CRUD operations."""
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.security import get_password_hash


# -------------------------------
# USER CRUD
# -------------------------------


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get a user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get a user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user with hashed password."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# -------------------------------
# TODO CRUD
# -------------------------------


def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    """Get a todo by ID."""
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos_by_user(db: Session, user_id: int) -> List[models.Todo]:
    """Get all todos for a specific user."""
    return db.query(models.Todo).filter(models.Todo.user_id == user_id).all()


def create_todo(db: Session, todo: schemas.TodoCreate) -> models.Todo:
    """Create a new todo."""
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoCreate) -> models.Todo:
    """Update an existing todo."""
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    for key, value in todo_update.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> None:
    """Delete a todo."""
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
