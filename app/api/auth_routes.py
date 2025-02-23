from datetime import timedelta, datetime

import pytz
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.testing.suite.test_reflection import users

from app.db.database import get_db
from app.services.UserService import UserService
from app.core.security import decode_access_token
from app.models.User import User
from fastapi import Response
from fastapi.responses import JSONResponse
auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# Register route to accept form data for username and password
@auth_router.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = UserService.create_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"message": "User registered successfully"}



def getUtcDate():
    sessionDate = datetime.now()
    sessionDate += timedelta(minutes=2)
    return sessionDate.strftime('%a, %d %b %Y %H:%M:%S GMT')
@auth_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), response: Response=None):
    user = UserService.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = UserService.generate_token(user)

    # Set the cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # Only use this in production (HTTPS)
        max_age=3600,  # Access token expires in 1 hour
        expires=getUtcDate()  # UTC-aware datetime
    )
    return JSONResponse(content={"message": access_token})


@auth_router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = db.query(User).filter(User.username==username).first()  # Fixed typo here
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {"username": user.username}