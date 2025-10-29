import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, get_key


# Load environment variables
load_dotenv()

# Get database URL directly from .env
DATABASE_URL = os.getenv("DATABASE_URL") or get_key("../.env", "DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()
