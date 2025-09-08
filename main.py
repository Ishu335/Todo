from fastapi import FastAPI
import models
from database import engine, SessionLocal
from routers import auth,todos,admin,user


app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
