#models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UserDb(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("TodoDb", back_populates="user")



class TodoDb(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UserDb", back_populates="todos")





