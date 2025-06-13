# File: app/cruds/user_crud.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import bcrypt

from app.models import UserDb
from app.schemas.user_schemas import UserCreate, UserUpdate
from passlib.context import CryptContext

bcrypt.__about__ = bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

    
def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
    """
    Retrieve a user by ID.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        UserDb: The user object if found.

    Raises:
        HTTPException: If the user is not found (404).
    """
    user = db.query(UserDb).filter(UserDb.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




def create_user(db: Session, user: UserCreate):
    """
    Create a new user.

    Args:
        db (Session): SQLAlchemy database session.
        user (UserCreate): User data from the request.

    Returns:
        UserDb: The newly created user object.
    """
    existing_user = db.query(UserDb).filter(UserDb.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_hashed_password(user.password)

    db_user = UserDb(
        email=user.email,
        username=user.username,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """
    Delete a user by ID.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): The ID of the user to delete.

    Returns:
        UserDb | None: The deleted user object if found and deleted, otherwise None.

    Raises:
        HTTPException: If the user is not found (404).
    """
    db_user = db.query(UserDb).filter(UserDb.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate):
    """
    Update an existing user by ID.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): The ID of the user to update.
        user (UserUpdate): The new user data.

    Returns:
        UserDb: The updated user object.
    """
    db_user = db.query(UserDb).filter(UserDb.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Handle password hashing if password is being updated
    update_data = user.model_dump(exclude_unset=True)  # Only get fields that were actually set
    if 'password' in update_data and update_data['password'] is not None:
        update_data['password'] = get_hashed_password(update_data['password'])
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(db: Session, password: str, email: str):
    """
    Authenticate a user with email and password.

    Args:
        db (Session): SQLAlchemy database session.
        password (str): Plain text password.
        email (str): User's email address.

    Returns:
        UserDb: The authenticated user object.

    Raises:
        HTTPException: If user not found or password is incorrect.
    """
    user = db.query(UserDb).filter(UserDb.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return user

