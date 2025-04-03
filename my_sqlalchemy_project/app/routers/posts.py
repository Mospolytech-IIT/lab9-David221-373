from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db

# Создаем экземпляр роутера
router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/{user_id}", response_model=schemas.Post)
def create_post_for_user(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    """Создать пост для пользователя"""
    return crud.create_user_post(db=db, post=post, user_id=user_id)

@router.get("/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех постов"""
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@router.get("/user/{user_id}", response_model=List[schemas.Post])
def read_user_posts(user_id: int, db: Session = Depends(get_db)):
    """Получить посты конкретного пользователя"""
    posts = crud.get_user_posts(db, user_id=user_id)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")
    return posts

@router.put("/{post_id}")
def update_post(post_id: int, new_content: str, db: Session = Depends(get_db)):
    """Обновить содержимое поста"""
    post = crud.update_post_content(db, post_id=post_id, new_content=new_content)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Удалить пост"""
    post = crud.delete_post(db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}