from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta, datetime, timezone
import secrets

router = APIRouter()

SCREAT_KEY = '7c6e7f0f826d65ba4f3c82838c92b1cfa26efc4377b30f337465a286782d0226'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    frist_name: str
    last_name: str
    hashed_password: str
    role: str

class Token(BaseModel):
    access_token: str   
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    users = db.query(Users).filter(Users.username == username).first()
    if not users:
        return False
    if not bcrypt_context.verify(password, users.hashed_password):
        return False
    return users


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, "id": user_id}  # ✅ Fixed: use "id" as string
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SCREAT_KEY, algorithm=ALGORITHM)


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, creted_user_request: CreateUserRequest):
    create_user_model = Users(
        email=creted_user_request.email,
        username=creted_user_request.username,
        frist_name=creted_user_request.frist_name,
        last_name=creted_user_request.last_name,
        role=creted_user_request.role,
        hashed_password=bcrypt_context.hash(creted_user_request.hashed_password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()


@router.post("/tooken", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Failed Authentication")  # ✅ Proper error
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}  # ✅ Now matches mo del

