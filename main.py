from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from typing import Annotated
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_all(db:Annotated[Session,Depends(get_db)]):
   return db.query(models.Todo).all()