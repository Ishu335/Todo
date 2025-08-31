from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
import models
from typing import Annotated
from database import engine, SessionLocal
from routers import auth


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


from pydantic import BaseModel, Field

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    # ✅ FIX: Ensure query returns list, not ORM objects directly
    return db.query(models.Todos).all()


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Id not found.")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = models.Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)   # ✅ FIX: refresh to get new ID
    return todo_model


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_data(db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo is Not Found")
    else:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)   # ✅ FIX: refresh after update


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()
