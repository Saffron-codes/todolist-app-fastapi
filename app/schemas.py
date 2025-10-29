from pydantic import BaseModel, EmailStr
from typing import Optional, List


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoCreate(TodoBase):
    user_id: int  # Used for legacy compatibility


class TodoCreateAuth(TodoBase):
    """Todo creation schema for authenticated users (no user_id needed)."""
    pass


class Todo(TodoBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    todos: List[Todo] = []

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
