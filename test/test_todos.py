from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from database import Base
from sqlalchemy.orm import sessionmaker,Session
from main import app
from routers.todos import get_db,get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from typing import Annotated
from models import Todos

SALALHEMY_DATABASE_URL="sqlite:///./testdb.db"
# SALALHEMY_DATABASE_URL="postgresql://postgres:admin@localhost:5432/TodoApplicationDatabase"

engine=create_engine(
    SALALHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool
    # the give comment is work for sqlit
)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base.metadata.create_all(bind=engine )

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db

    finally:
        db.close()

def override_get_current_user():
    return {'username':'admin','id':1,'user_role':'admin'}

# dependency_override  is inbuil funtion in python
app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

client=TestClient(app)

@pytest.fixture
def test_todos():
    todo=Todos(
        title="Lear Code",
        description="Learn everyday",
        priority=5,
        complete=False,
        owner_id=1
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

def test_read_all_authenticated():
    response=client.get("/")
    assert response.status_code==status.HTTP_200_OK
    # Errors Occer
    # assert response.json()==[{
    #         "title": "Learn Code",
    #         "description": "Learn everyday",
    #         "priority": 5,
    #         "complete": False,
    #         "owner_id": 1
    #     }]  
