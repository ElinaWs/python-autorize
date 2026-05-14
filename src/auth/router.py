from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig, TokenPayload
from sqlalchemy import or_

from src.database import get_db
from src.models.user import User
from src.auth.schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserOutSchema
)

security = HTTPBearer()

config = AuthXConfig(
    JWT_SECRET_KEY="test-secret-key",
    JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(config=config)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegisterSchema,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        or_(
            User.username == user_data.username,
            User.email == user_data.email
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь уже существует"
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Регистрация успешна"
    }


@user_router.post("/login")
def login(
    user_data: UserLoginSchema,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        or_(
            User.username == user_data.login,
            User.email == user_data.login
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль"
        )

    if user.password != user_data.password:
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль"
        )

    access_token = auth.create_access_token(uid=str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@user_router.get("/me", response_model=UserOutSchema)
def get_me(
    payload: TokenPayload = Depends(auth.access_token_required),
    credentials=Depends(security),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == int(payload.sub)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return user


@user_router.get("/protected")
def protected(
    payload: TokenPayload = Depends(auth.access_token_required),
    credentials=Depends(security),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == int(payload.sub)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return {
        "message": "Вы авторизованы",
        "token": credentials.credentials,
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }