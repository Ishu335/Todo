from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# Database URL (SQLite in this case)
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/TodoApplicationDatabase" <== Postgread SSQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:mysql@localhost:3306/TodoApplicationDatabase"  #<== MYSQSL



# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,   # We commit manually with session.commit()
    autoflush=False,    # Changes are not flushed to DB until commit
    bind=engine         # Bind session to our engine
)

# Base class for ORM models
Base = declarative_base()

