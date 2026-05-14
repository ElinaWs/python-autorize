from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig, TokenPayload

from src.database import get_db
from src.models.user import User
from src.auth.schemas import UserRegisterSchema, UserLoginSchema, RefreshSchema

security = HTTPBearer(auto_error=False)

config = AuthXConfig(
    JWT_SECRET_KEY="test-secret-key",
    JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(config=config)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ---------------- REGISTER ----------------

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserRegisterSchema,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким логином уже существует"
        )

    new_user = User(
        username=user_data.username,
        password=user_data.password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Регистрация прошла успешно"
    }


# ---------------- LOGIN ----------------

@user_router.post("/login")
def login(
    user_data: UserLoginSchema,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == user_data.username
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
    refresh_token = auth.create_refresh_token(uid=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ---------------- REFRESH ----------------

@user_router.post("/refresh")
def refresh(user_data: RefreshSchema):
    try:
        payload = auth.verify_token(user_data.refresh_token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Неверный refresh token"
        )

    new_access_token = auth.create_access_token(uid=payload.sub)

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


# ---------------- PROTECTED ----------------

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
        "message": f"Аккаунт найден: {user.username}",
        "token": credentials.credentials,
        "user_info": {
            "id": user.id,
            "username": user.username
        }
    }