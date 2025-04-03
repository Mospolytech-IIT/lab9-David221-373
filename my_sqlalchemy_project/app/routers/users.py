from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db  # Убедитесь, что импорт правильный

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):  # Добавьте Depends
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список пользователей"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по ID"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя и все его посты"""
    db_user = crud.delete_user_and_posts(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User and all their posts deleted successfully"}