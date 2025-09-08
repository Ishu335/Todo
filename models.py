# This defines a SQLAlchemy ORM model for the "todos" table
from database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey

class Users(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    email=Column(String,unique=True)
    username = Column(String, unique=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password = Column(String)
    is_active=Column(Boolean,default=True)
    role=Column(String)
    phone_number=Column(String(10))

class Todos(Base):  
    __tablename__ = "todos"   # Table name in the database
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, default=0)
    complete = Column(Boolean, default=False)
    owner_id=Column(Integer,ForeignKey("users.id"))
