from fastapi import APIRouter, Depends, HTTPException, status, Path,Request,status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from Todo.database import  SessionLocal
# import models
from .auth  import get_current_user
from Todo.models import Todos
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="Todo/templates")
router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def redirect_to_login():
    response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

# This class is Used for Validation 
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)

# Pages
@router.get('/todo-page') 
async def render_todo_page(requeest:Request,db:db_dependency):
    try:
        user=await get_current_user(requeest.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todos=db.query(Todos).filter("todo.html",{"request":request,"todos":todos,"user":user})
        return templates.TemplateResponse("todo.html",{"request":request,"todos":todos,"user":user})
    except:
        return redirect_to_login()


# Read all the books in Database
@router.get("/all_todos", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db: db_dependency):
    # Ensure query returns list, not ORM objects directly
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todos not found.")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency, db: db_dependency, 
                      todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    todo_model = Todos(**todo_request.dict(),owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)   # refresh to get new ID
    return todo_model


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todos(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo is Not Found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()