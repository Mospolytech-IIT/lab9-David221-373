from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi import FastAPI, Depends
from . import models
from .database import engine, get_db
from .routers import users, posts
# Создаем таблицы (обычно это делается через миграции, но для простоты оставим здесь)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router, prefix="/users")
app.include_router(posts.router)
# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Подключаем роутеры
from app.routers import posts_router, users_router
app.include_router(posts_router)
app.include_router(users_router)




@app.get("/")
def read_root():
    return {"message": "Welcome to the SQLAlchemy-FastAPI example!"}