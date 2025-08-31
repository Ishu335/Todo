# 📝 Todo API with FastAPI

A simple **Todo application API** built with **FastAPI** and **SQLite**.  
This project demonstrates CRUD operations (Create, Read, Update, Delete) for managing tasks using modern Python backend development practices.

---

## 🚀 Features

- Create a new todo item ✅  
- View all todos 📋  
- Update an existing todo ✏️  
- Delete a todo ❌  
- Lightweight database with **SQLite**  
- Modular project structure with **FastAPI Routers**  

---

## 📂 Project Structure
```
Todo/
│── app/
│   │── __init__.py
│   │── main.py            # FastAPI app entry point
│   │── database.py        # Database setup (SQLAlchemy/SQLite)
│   │── models.py          # SQLAlchemy models
│   │── schemas.py         # Pydantic models (request/response validation)
│   │── crud.py            # Database CRUD operations
│   │── routers/           # API endpoints
│   │   │── __init__.py
│   │   │── todo.py        # Todo routes (GET, POST, PUT, DELETE)
│   │── core/              # Core configurations
│   │   │── config.py      # Settings (env vars, constants)
│
│── tests/                 # Unit & integration tests
│   │── test_todo.py
│
│── requirements.txt       # Project dependencies
│── README.md              # Project documentation
│── .gitignore             # Ignore venv, cache, DB, etc.
│── testapp.db             # SQLite database (ignored in production)

```

