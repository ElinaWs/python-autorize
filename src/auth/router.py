from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig, TokenPayload

from src.database import get_db
from src.models.user import User
from src.auth.schemas import UserRegisterSchema


config = AuthXConfig(
    JWT_SECRET_KEY="test-secret-key",
    JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(config=config)
security = HTTPBearer()

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserRegisterSchema,    
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким логином уже существует"
        )
    
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует"
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,   
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)              

    return {
        "message": "Регистрация прошла успешно"
    }

@user_router.post("/login")
def login(
    username: str,          
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or user.password != password:
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль"
        )

    access_token = auth.create_access_token(uid=str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@user_router.post("/access")
def get_refresh(
    payload: TokenPayload = Depends(auth.access_token_required)
):
    refresh_token = auth.create_refresh_token(uid=payload.sub)
    return {
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@user_router.get("/protected")
def protected(
    payload: TokenPayload = Depends(auth.refresh_token_required),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == int(payload.sub)).first()
    if not user:
         raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
    
    return {
        "message": f"Аккаунт найден: {user.username}",
        "user_info": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }