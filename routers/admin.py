from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from database import  SessionLocal
import models
from .auth  import get_current_user
from models import Todos

router = APIRouter(
    prefix='/admin'
    ,tags=['admin']
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_all( user:user_dependency,db:db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(Todos).all()