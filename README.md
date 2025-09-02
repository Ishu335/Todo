# ✅ FastAPI Todo App

A fully functional **Todo API** built with **FastAPI**, featuring:

- Secure **JWT Authentication**
- Input **validation** with Pydantic
- Password **hashing**
- **User registration and login**
- Full **CRUD operations** on todos

---

## 📌 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Setup & Run](#setup--run)
- [Authentication](#authentication)
- [Validation & Verification](#validation--verification)
- [API Endpoints](#api-endpoints)
- [Security Notes](#security-notes)
- [License](#license)

---

## 🚀 Features

- 🧑‍💻 User Signup & Login
- 🔐 Secure JWT tokens (expirable)
- ✅ Input validation with Pydantic
- 🔑 Password hashing using `passlib[bcrypt]`
- 🗃️ SQLAlchemy ORM for database
- 📄 Interactive API docs at `/docs`

---

## 📁 Project Structure
```
Todo/
├── main.py # App entry point
├── models.py # SQLAlchemy models
├── database.py # DB setup
├── routers/
│ ├── auth.py # User login & JWT logic
│ └── todos.py # Todo CRUD logic
├── schemas/ # Pydantic models (BaseModel)
├── utils/ # Utility functions (optional)
├── README.md
└── requirements.txt
```

---

## 🛠 Tech Stack

- **Python 3.10+**
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Passlib](https://passlib.readthedocs.io/)
- [Python-JOSE](https://python-jose.readthedocs.io/en/latest/) (for JWT)
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)

---

## ⚙️ Setup & Run

1. **Clone the repo:**
```
git clone https://github.com/Ishu335/Todo.git
cd Todo
```





