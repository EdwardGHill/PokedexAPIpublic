from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from connection import get_db
from user import User, UserCreate, UserResponse
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from api.models import Collection, Favorite

router = APIRouter()

SECRET_KEY = "Secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Token creation function
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with db as session:
        user = session.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception

    return user

class TokenWithUsername(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

@router.post("/token", response_model=TokenWithUsername)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        with db as session:
            user = session.query(User).filter(User.username == form_data.username).first()

            if user is None or not user.verify_password(form_data.password):
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

            # Include the username in the response
            return {"access_token": access_token, "token_type": "bearer", "username": user.username}
    except Exception as e:
        # Log the exception or handle it accordingly
        raise e

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        with db as session:
            db_user = User(username=user.username, email=user.email)
            db_user.set_password(user.password)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)

        # Create an instance of UserResponse with relevant information
        response_user = UserResponse(id=db_user.id, username=db_user.username, email=db_user.email)

        return response_user
    except IntegrityError as e:
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(status_code=400, detail="DUPLICATE_USER_EMAIL")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/delete-account", status_code=204)
def delete_user_account(current_user: User = Depends(get_current_user)):
    db = get_db()
    try:
        with db as session:
            # Cascade delete favorites and collections
            session.query(Favorite).filter_by(user_id=current_user.id).delete()
            session.query(Collection).filter_by(user_id=current_user.id).delete()

            # Delete the user
            session.delete(current_user)
            session.commit()

        return None  # Return None for a 204 response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.__exit__(None, None, None)