# file: app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user_schemas import User, UserCreate, UserUpdate, UserLogin, Token
from app.cruds import user_crud
from app.database import get_db
from app.models import UserDb
from app.auth.auth import create_access_token, oauth2_scheme


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db=db, user_id=user_id)
    return user


@router.post("/create", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, user=user)


@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = user_crud.delete_user(db=db, user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="user not found")
    return deleted_user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = user_crud.update_user(db=db, user_id=user_id, user=user)
    return updated_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.login_user(db=db, email=form_data.username, password=form_data.password)
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/form", response_model=Token)
def login_auth(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)):
    
    user = user_crud.login_user(db=db, email=email, password=password)
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}