from fastapi import APIRouter


from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from database import  SessionLocal
import models
from .auth  import get_current_user
from models import Todos
from passlib.context import CryptContext

router=APIRouter(
     prefix='/user' 
    ,tags=['user']
)

class Change_pass(BaseModel):
    passWord: str 
    newPassword:str=Field(min_length=3)

class Update_Phone_num(BaseModel):
    phone_number:str=Field(min_length=1,max_length=10)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get("/")
async def get_user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    else:
        return db.query(models.Users).filter(models.Users.id==user.get('id')).first()   
    

@router.put("/change_password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency,db:db_dependency,passChage_request:Change_pass = Body()):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')

    change_pass=db.query(models.Users).filter(models.Users.id==user.get('id')).first()

    if not bcrypt_context.verify(passChage_request.passWord,change_pass.hashed_password):
        raise HTTPException(status_code=401,detail='Error on password change')
    change_pass.hashed_password=bcrypt_context.hash(passChage_request.newPassword)
    db.add(change_pass)         
    db.commit()

@router.put("/phone_number",status_code=status.HTTP_204_NO_CONTENT)
async def add_phone_number(user:user_dependency,db:db_dependency,phone_number:Update_Phone_num=Body()):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    add_phone=db.query(models.Users).filter(models.Users.id==user.get('id')).first()
    add_phone.phone_number=phone_number.phone_number
    db.add(add_phone) 
    db.commit()
    


    