from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database URL (SQLite in this case)
SQLALCHEMY_DATABASE_URL = "sqlite:///./testapp.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed only for SQLite
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,   # We commit manually with session.commit()
    autoflush=False,    # Changes are not flushed to DB until commit
    bind=engine         # Bind session to our engine
)

# Base class for ORM models
Base = declarative_base()
