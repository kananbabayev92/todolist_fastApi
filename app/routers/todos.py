# File: app/routers/todos.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.todo_schemas import Todo, TodoCreate, Todoupdate
from app.database import get_db
from app.models import TodoDb
from app.cruds import todos_crud
from app.models import UserDb
from app.auth.auth import get_current_user


router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=list[Todo])
def read_todos(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: UserDb = Depends(get_current_user)
):
    """Get all todos for the current user with pagination"""
    return todos_crud.get_all_todos(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.post("/newtodos", response_model=Todo)
def create_todo(
    todo: TodoCreate, 
    db: Session = Depends(get_db), 
    current_user: UserDb = Depends(get_current_user)
):
    """Create a new todo for the current user"""
    return todos_crud.create_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/{todo_id}", response_model=Todo)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: UserDb = Depends(get_current_user)
):
    """Get a specific todo by ID for the current user"""
    return todos_crud.get_todo(db=db, todo_id=todo_id, user_id=current_user.id)


@router.put("/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int, 
    todo: Todoupdate, 
    db: Session = Depends(get_db),
    current_user: UserDb = Depends(get_current_user)
):
    """Update an existing todo for the current user"""
    return todos_crud.update_todo(db=db, todo_id=todo_id, todo=todo, user_id=current_user.id)


@router.delete("/{todo_id}", response_model=Todo)
def delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: UserDb = Depends(get_current_user)
):
    """Delete a todo by ID for the current user"""
    return todos_crud.delete_todo(db=db, todo_id=todo_id, user_id=current_user.id)


@router.get("/completed/all", response_model=list[Todo])
def get_completed_todos(
    db: Session = Depends(get_db),
    current_user: UserDb = Depends(get_current_user)
):
    """Get all completed todos for the current user"""
    return todos_crud.get_completed_todos(db=db, user_id=current_user.id)