from pydantic import BaseModel, EmailStr


# Базовые схемы
class UserBase(BaseModel):
    username: str
    email: EmailStr


class PostBase(BaseModel):
    title: str
    content: str


# Схемы для создания
class UserCreate(UserBase):
    password: str


class PostCreate(PostBase):
    pass


# Схемы для ответов (не включают чувствительные данные)
class User(UserBase):
    id: int

    class Config:
        orm_mode = True  # Позволяет работать с ORM объектами


class Post(PostBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True



