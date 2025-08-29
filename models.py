# This defines a SQLAlchemy ORM model for the "todos" table
from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):  
    __tablename__ = "todos"   # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, default=0)
    complete = Column(Boolean, default=False)
