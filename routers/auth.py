from fastapi import APIRouter,status,Depends
from pydantic import BaseModel
from  models import Users
from passlib.context import CryptContext
from database import SessionLocal  # Make sure this import matches your project structure
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter()
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')



class CreateUserRequest(BaseModel):
    username:str
    email:str
    frist_name:str
    last_name:str
    hashed_password:str
    role:str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session,Depends(get_db)]

@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,
                       creted_user_request:CreateUserRequest):
    create_user_model=Users(
        email=creted_user_request.email,
        username=creted_user_request.username,
        frist_name=creted_user_request.frist_name,
        last_name=creted_user_request.last_name,
        role=creted_user_request.role,
        hashed_password=bcrypt_context.hash(creted_user_request.hashed_password),
        is_active=True
        )
    # raise HTTP_ss
    db.add(create_user_model)
    db.commit()
