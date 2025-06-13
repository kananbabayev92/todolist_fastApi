#file: app/auth/auth.py
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user_schemas import UserLogin
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserDb

SECRET_KEY = "your_secret_key"  # Change this to a secure random key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = str(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        return int(user_id)
    except JWTError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    invalid_login_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate login",
        headers={"WWW-Authenticate": "Bearer"}
    )
    user_id = verify_token(token, invalid_login_error)
    user = db.query(UserDb).filter(UserDb.id == user_id).first()
    if user is None:
        raise invalid_login_error
    return user

