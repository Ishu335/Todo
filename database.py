from sqlalchemy import create_engine
from sqlalchemy import sessionMaker
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
     connect_args={"check_same_thread": False}  # this false : only allowed to create 1 connection at a time or 1 thread
     )
SessionLocal=sessionMaker(
    autocommit=False,# sesson perform sone this automaticaly 
    autoFlash=False,# so we make it False 
    bind=engine # binding the session with engine
    )