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
db_dependency = Annotated[Session, Depends(get_db)]
@app.get("/")
async def read_all(db:db_dependency):
   return db.query(models.Todo).all()