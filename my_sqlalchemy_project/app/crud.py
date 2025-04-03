from sqlalchemy.orm import Session
from . import models, schemas

# Операции с пользователями
def get_user(db: Session, user_id: int):
    """Получить пользователя по ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Получить пользователя по email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получить список пользователей с пагинацией"""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Создать нового пользователя"""
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password  # В реальном приложении пароль должен быть хеширован!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Операции с постами
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    """Получить список постов с пагинацией"""
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_user_posts(db: Session, user_id: int):
    """Получить посты конкретного пользователя"""
    return db.query(models.Post).filter(models.Post.user_id == user_id).all()

def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    """Создать новый пост для пользователя"""
    db_post = models.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post_content(db: Session, post_id: int, new_content: str):
    """Обновить содержимое поста"""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db_post.content = new_content
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    """Удалить пост"""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post

def delete_user_and_posts(db: Session, user_id: int):
    """Удалить пользователя и все его посты"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        # Удаляем все посты пользователя
        db.query(models.Post).filter(models.Post.user_id == user_id).delete()
        # Удаляем пользователя
        db.delete(db_user)
        db.commit()
    return db_user