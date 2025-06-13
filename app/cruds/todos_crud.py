# file: app/cruds/todos_crud.py

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas import todo_schemas
from app.models import TodoDb
from app.schemas.todo_schemas import Todo, Todoupdate
from app.models import UserDb


def get_todo(db: Session, todo_id: int, user_id: int):
    # Get a specific todo by id for the current user
    todo = db.query(TodoDb).filter(
        TodoDb.id == todo_id, 
        TodoDb.user_id == user_id
    ).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


def get_all_todos(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    # Get all todos for the current user with pagination
    all_todos = db.query(TodoDb).filter(
        TodoDb.user_id == user_id
    ).offset(skip).limit(limit).all()
    return all_todos


def create_todo(db: Session, todo: todo_schemas.TodoCreate, user_id: int):
    # Create a new todo and associate it with the current user
    db_todo = models.TodoDb(
        title=todo.title, 
        description=todo.description, 
        completed=todo.completed,
        user_id=user_id  # Associate todo with the user
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: Todoupdate, user_id: int):
    """ Update a specific todo by id for the current user.
    Args:
        db (Session): SQLAlchemy database session
        todo_id (int): The ID of the todo to update
        todo (Todoupdate): The todo data to update
        user_id (int): The ID of the current user
    Returns:
        TodoDb: The updated todo object
    """
    db_todo = db.query(TodoDb).filter(
        TodoDb.id == todo_id,
        TodoDb.user_id == user_id  # Ensure user owns this todo
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Only update fields that are not None
    update_data = todo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo
    

def delete_todo(db: Session, todo_id: int, user_id: int):
    """ Delete a specific todo by id for the current user.
    Args:
        db (Session): SQLAlchemy database session
        todo_id (int): The ID of the todo to delete
        user_id (int): The ID of the current user
    Returns:
        TodoDb: The deleted todo object
    """
    db_todo = db.query(TodoDb).filter(
        TodoDb.id == todo_id,
        TodoDb.user_id == user_id  # Ensure user owns this todo
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return db_todo


def get_completed_todos(db: Session, user_id: int):
    """ Get all completed todos for the current user.
    Args:
        db (Session): SQLAlchemy database session
        user_id (int): The ID of the current user
    Returns:
        List[TodoDb]: List of completed todos
    """
    todos = db.query(TodoDb).filter(
        TodoDb.completed == True,
        TodoDb.user_id == user_id
    ).all()
    return todos