from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# Модель User представляет таблицу users в базе данных
class User(Base):
    __tablename__ = "users"  # Имя таблицы в базе данных

    # Поля таблицы
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)

    # Связь один-ко-многим с таблицей posts
    posts = relationship("Post", back_populates="owner")


# Модель Post представляет таблицу posts в базе данных
class Post(Base):
    __tablename__ = "posts"  # Имя таблицы в базе данных

    # Поля таблицы
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), index=True, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Связь многие-к-одному с таблицей users
    owner = relationship("User", back_populates="posts")