from fastapi import APIRouter,status
from pydantic import BaseModel
from  models import Users
from passlib.context import CryptContext

router = APIRouter()
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')



class CreateUserRequest(BaseModel):
    username:str
    email:str
    frist_name:str
    last_name:str
    hashed_password:str
    role:str

@router.post("/auth/")
async def create_user(creted_user_request:CreateUserRequest,status_code=status.HTTP_201_CREATED):
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
    return create_user_model
